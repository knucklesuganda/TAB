import logging

main_logger = logging.getLogger("information")
main_logger.setLevel(logging.INFO)

file_handler = logging.FileHandler("information.log")
file_handler.setFormatter(logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s"))
main_logger.addHandler(file_handler)

__all__ = ['main_logger']
