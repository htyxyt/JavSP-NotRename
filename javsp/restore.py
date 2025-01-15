"""整理文件后恢复文件名的相关功能"""
import os
from datetime import datetime
import logging

logger = logging.getLogger('main')

def record_file_metadata(file_path, new_file_path, file_metadata):
    """记录文件的原始文件名、大小和最后修改时间"""
    try:
        file_size = os.path.getsize(file_path)
        file_mtime = datetime.fromtimestamp(os.path.getmtime(file_path)).strftime('%Y-%m-%d %H:%M:%S')
        file_metadata[os.path.basename(file_path)] = {
            'original_name': os.path.basename(file_path),
            'new_path': new_file_path,
            'size': file_size,
            'mtime': file_mtime
        }
        logger.debug(f"记录文件元数据: {file_path}")
    except Exception as e:
        logger.error(f"记录文件元数据失败: {e}")

def restore_original_filenames(movie, file_metadata):
    """恢复文件的原始名称"""
    try:
        save_dir = movie.save_dir
        for original_filename, metadata in file_metadata.items():
            found = False
            new_filepath = os.path.join(os.path.dirname(movie.nfo_file), original_filename)
            
            # 在 save_dir 中查找文件
            for filename in os.listdir(save_dir):
                current_filepath = os.path.join(save_dir, filename)
                
                if not os.path.exists(current_filepath):
                    continue
                
                file_size = os.path.getsize(current_filepath)
                file_mtime = datetime.fromtimestamp(os.path.getmtime(current_filepath)).strftime('%Y-%m-%d %H:%M:%S')
                
                if file_size == metadata['size'] and file_mtime == metadata['mtime']:
                    found = True
                    break
            
            if found:
                try:
                    os.rename(current_filepath, new_filepath)
                    logger.info(f"成功恢复文件名: {original_filename}\n")
                except OSError as e:
                    logger.error(f"重命名文件 {current_filepath} 失败: {e}\n")
            else:
                logger.warning(f"在 {save_dir} 中找不到匹配的文件: {original_filename}\n")
    except Exception as e:
        logger.error(f"恢复文件名失败: {e}\n")
