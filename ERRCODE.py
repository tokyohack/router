class MemoryIsOverflow_Exception(Exception):
    def __str__(self):
        return 'メモリーエラー、メモリ容量を増やしてください。\n終了します。'
