# !/usr/bin/env python3
# exceptions.py
class MemoryIsOverflow_Exception(Exception):
    """メモリ容量が不足した場合に発生する例外"""

    def __str__(self) -> str:  # 戻り値の型を明示的に指定
        return "メモリーエラー、メモリ容量を増やしてください。\n終了します。"


class MaxRetryError(Exception):
    """メモリ関連の例外の基底クラス"""

    def __str__(self) -> str:  # 戻り値の型を明示的に指定
        return "MaxRetryError。\n終了します。"


class InvalidCredentialsError(Exception):
    """認証エラーの例外クラス"""

    def __str__(self) -> str:  # 戻り値の型を明示的に指定
        return "認証エラー。無効なユーザーIDか無効なパスワードです。\n終了します。"


class router_Exception(Exception):
    pass


class token_err(router_Exception):
    """認証エラーの例外クラス"""

    def __str__(self) -> str:  # 戻り値の型を明示的に指定
        return "ルータのトークンを取得できませんでした。\n終了します。"
