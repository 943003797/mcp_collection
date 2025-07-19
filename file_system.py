"""
文件系统操作工具类
"""
import shutil
import os

class FileSystem:
    """
    文件系统操作类
    """
    
    @staticmethod
    def copy_dir(from_path: str, to_path: str) -> str:
        """
        复制目录
        
        参数:
            src: 源目录路径
            dst: 目标目录路径
        """
            # 如果源目录不存在就退出
        if not os.path.isdir(from_path):
            raise FileNotFoundError(f'源目录不存在: {from_path}')

        # 创建目标目录
        os.makedirs(to_path, exist_ok=True)

        # 复制所有文件（包含子目录）
        for root, _, files in os.walk(from_path):
            # 计算目标路径
            relative_path = os.path.relpath(root, from_path)
            target_dir = os.path.join(to_path, relative_path)
            
            # 创建目标子目录
            os.makedirs(target_dir, exist_ok=True)
            
            # 复制当前目录下的所有文件
            for file in files:
                src_file = os.path.join(root, file)
                dst_file = os.path.join(target_dir, file)
                shutil.copy2(src_file, dst_file)

        return "success"