from __future__ import annotations

"""Armazena a senha do MySQL no Gerenciador de Credenciais do Windows.

Nenhum segredo é escrito em database.json, logs, cenas, saves ou repositório.
O Windows protege a credencial para o usuário que está executando o Aetheria.
"""

import ctypes
import sys
from ctypes import wintypes

from .config import DatabaseSettings


CRED_TYPE_GENERIC = 1
CRED_PERSIST_LOCAL_MACHINE = 2
ERROR_NOT_FOUND = 1168


class CredentialStoreError(RuntimeError):
    pass


class _CredentialW(ctypes.Structure):
    _fields_ = [
        ("Flags", wintypes.DWORD),
        ("Type", wintypes.DWORD),
        ("TargetName", wintypes.LPWSTR),
        ("Comment", wintypes.LPWSTR),
        ("LastWritten", wintypes.FILETIME),
        ("CredentialBlobSize", wintypes.DWORD),
        ("CredentialBlob", ctypes.POINTER(ctypes.c_ubyte)),
        ("Persist", wintypes.DWORD),
        ("AttributeCount", wintypes.DWORD),
        ("Attributes", ctypes.c_void_p),
        ("TargetAlias", wintypes.LPWSTR),
        ("UserName", wintypes.LPWSTR),
    ]


class WindowsCredentialStore:
    PREFIX = "Aetheria/MySQL"

    @classmethod
    def available(cls) -> bool:
        return sys.platform == "win32" and hasattr(ctypes, "WinDLL")

    @classmethod
    def target_name(cls, settings: DatabaseSettings) -> str:
        host = settings.host.strip().casefold() or "127.0.0.1"
        user = settings.user.strip().casefold() or "root"
        database = settings.database.strip().casefold() or "aetheria_rpg"
        return f"{cls.PREFIX}/{host}:{int(settings.port)}/{database}/{user}"

    @classmethod
    def _advapi32(cls):
        if not cls.available():
            raise CredentialStoreError("O Gerenciador de Credenciais está disponível somente no Windows.")
        library = ctypes.WinDLL("Advapi32.dll", use_last_error=True)
        library.CredWriteW.argtypes = [ctypes.POINTER(_CredentialW), wintypes.DWORD]
        library.CredWriteW.restype = wintypes.BOOL
        library.CredReadW.argtypes = [
            wintypes.LPCWSTR,
            wintypes.DWORD,
            wintypes.DWORD,
            ctypes.POINTER(ctypes.POINTER(_CredentialW)),
        ]
        library.CredReadW.restype = wintypes.BOOL
        library.CredDeleteW.argtypes = [wintypes.LPCWSTR, wintypes.DWORD, wintypes.DWORD]
        library.CredDeleteW.restype = wintypes.BOOL
        library.CredFree.argtypes = [ctypes.c_void_p]
        library.CredFree.restype = None
        return library

    @classmethod
    def save(cls, settings: DatabaseSettings, password: str) -> None:
        if not password:
            raise CredentialStoreError("A senha vazia não será armazenada.")
        library = cls._advapi32()
        encoded = password.encode("utf-16-le")
        blob = (ctypes.c_ubyte * len(encoded)).from_buffer_copy(encoded)
        credential = _CredentialW()
        credential.Type = CRED_TYPE_GENERIC
        credential.TargetName = cls.target_name(settings)
        credential.Comment = "Senha MySQL salva pelo Aetheria RPG"
        credential.CredentialBlobSize = len(encoded)
        credential.CredentialBlob = ctypes.cast(blob, ctypes.POINTER(ctypes.c_ubyte))
        credential.Persist = CRED_PERSIST_LOCAL_MACHINE
        credential.UserName = settings.user
        if not library.CredWriteW(ctypes.byref(credential), 0):
            code = ctypes.get_last_error()
            raise CredentialStoreError(f"O Windows recusou salvar a credencial (código {code}).")

    @classmethod
    def load(cls, settings: DatabaseSettings) -> str:
        if not cls.available():
            return ""
        library = cls._advapi32()
        pointer = ctypes.POINTER(_CredentialW)()
        if not library.CredReadW(
            cls.target_name(settings), CRED_TYPE_GENERIC, 0, ctypes.byref(pointer),
        ):
            code = ctypes.get_last_error()
            if code == ERROR_NOT_FOUND:
                return ""
            raise CredentialStoreError(f"O Windows recusou ler a credencial (código {code}).")
        try:
            credential = pointer.contents
            if not credential.CredentialBlob or not credential.CredentialBlobSize:
                return ""
            raw = ctypes.string_at(credential.CredentialBlob, credential.CredentialBlobSize)
            return raw.decode("utf-16-le")
        finally:
            library.CredFree(pointer)

    @classmethod
    def delete(cls, settings: DatabaseSettings) -> bool:
        if not cls.available():
            return False
        library = cls._advapi32()
        if library.CredDeleteW(cls.target_name(settings), CRED_TYPE_GENERIC, 0):
            return True
        code = ctypes.get_last_error()
        if code == ERROR_NOT_FOUND:
            return False
        raise CredentialStoreError(f"O Windows recusou apagar a credencial (código {code}).")
