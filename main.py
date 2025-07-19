from mcp.server.fastmcp import FastMCP
from file_system import FileSystem
from cosyvoice_v1 import Cosyvoice
from auto_cut import autoCut

mcp = FastMCP("mcp_collection", port=8000)

@mcp.tool()
def write_file(file_path: str, content: str) -> str:
    """
    Use this tool to write content to a specified file
    Parameters:
        file_path: Target file path
        content: Content to write
        
    Returns:
        str: Operation result string
        May raise:
            FileNotFoundError: When file path does not exist
            IOError: When write operation fails
    """
    return FileSystem.write_file(file_path, content)

@mcp.tool()
def copy_dir(from_path: str, to_path: str) -> str:
    """
    This tool is used to copy files from one directory to another. A new directory named with current timestamp will be created in the destination path, and all files (excluding subdirectories) from source directory will be copied to it.
    Parameters:
        from_path: Source directory path containing files to copy
        to_path: Destination directory path where files will be copied to
    Returns:
        success: When files are copied successfully
        FileNotFoundError: When source directory does not exist
    """
    return FileSystem.copy_dir(from_path, to_path)

@mcp.tool()
def create_text_to_audio(text: str, out_path: str) -> str:
    """
    This tool is used to convert text into audio. Input the text and the output directory, and the audio will be generated and saved to the specified directory.
    Parameters:
        text: String text
        out_path: Output directory for the audio
    Returns:
        Success: Operation success
        Failed: Operation failed
    """
    return Cosyvoice.generate_audio(text, out_path)

@mcp.tool()
def auto_cut(draft_path: str) -> str:
    """
    This tool can achieve automatic video editing by specifying the draft path
    Parameters:
        draft_path: Draft path
    Returns:
        success: When files are copied successfully
    """
    ac = autoCut(draft_path, '浮光.mp3','水墨山河.mp4');
    ac.general_draft();
    return "Success"

if __name__ == "__main__":
    # auto_cut('/Volumes/M0/AI/jianyingdraft/JianyingPro Drafts/千古词帝李煜的巅峰之作')
    mcp.run(transport='sse')