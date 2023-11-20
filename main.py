import os
import shutil
import whisper
from spleeter.separator import Separator
from pydub import AudioSegment
from pydub.silence import split_on_silence
import shutil


def split_audio(input_folder, output_folder, silence_threshold=-40, min_silence_len=1000):
    # 确保输出文件夹存在
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # 遍历输入文件夹中的每个音频文件
    for filename in os.listdir(input_folder):
        if filename.endswith('.mp3') or filename.endswith('.wav') or filename.endswith('.ogg') or filename.endswith('.aac'):
            input_path = os.path.join(input_folder, filename)
            
            # 加载音频文件
            audio = AudioSegment.from_wav(input_path)
            
            # 将音频文件按说话停顿分割
            segments = split_on_silence(audio, silence_thresh=silence_threshold, min_silence_len=min_silence_len)
            
            # 将分割后的片段保存到输出文件夹
            for i, segment in enumerate(segments):
                output_path = os.path.join(output_folder, f"{os.path.splitext(filename)[0]}_{i+1}.wav")
                segment.export(output_path, format="wav")

def a2t():
    result = model.transcribe("input/raw/a1.wav",language='Japanese')
    print(result["text"])

def transcribe_audio_to_text(input_folder, output_folder):
    # 确保输出文件夹存在
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # 遍历输入文件夹中的每个音频文件
    for filename in os.listdir(input_folder):
        if filename.endswith(".wav"):
            input_path = os.path.join(input_folder, filename)
            output_path = os.path.join(output_folder, f"{os.path.splitext(filename)[0]}.txt")

            # 使用Whisper进行语音转文本
            # result = model.transcribe(input_path,language=lan)
            result = model.transcribe(input_path)
            print(result["text"])

            # 提取并保存文本
            transcribed_text = result["text"]
            with open(output_path, "w", encoding="utf-8") as file:
                file.write(transcribed_text)


def spleeter_audio():
    # 初始化 Spleeter
    separator = Separator('spleeter:2stems')
    
    # 指定音频文件所在目录
    audio_directory = '.\\input\\raw'
    output = ".\\input\\separate"


    # 遍历指定目录下的所有文件
    for filename in os.listdir(audio_directory):
        if filename.endswith('.mp3') or filename.endswith('.wav') or filename.endswith('.ogg') or filename.endswith('.aac'):
            audio_file_path = os.path.join(audio_directory, filename)
            
            separator.separate_to_file(audio_file_path, output)
            
    source_directory = "input/separate"  # 源文件夹路径
    output_directory = "input/separate"  # 输出文件夹路径

    # 获取源文件夹下所有子文件夹的路径
    folders = [os.path.join(source_directory, folder) for folder in os.listdir(source_directory) if os.path.isdir(os.path.join(source_directory, folder))]

    # 遍历每个子文件夹
    for folder in folders:
        vocals_file = os.path.join(folder, 'vocals.wav')  # 获取每个子文件夹中的vocals.wav路径
        if os.path.isfile(vocals_file):
            # 获取当前文件夹名称作为新文件名
            folder_name = os.path.basename(folder)
            output_file = os.path.join(output_directory, f'{folder_name}.wav')  # 构建输出文件路径
            shutil.copy(vocals_file, output_file)  # 复制vocals.wav到输出文件夹并重命名为目录名
        shutil.rmtree(os.path.join(output_directory, folder_name))

            
if __name__ == "__main__":
    import multiprocessing
    multiprocessing.freeze_support()
    
    # 选择声音素材的语言
    # lan = ["Japanese","Chinese","English"][0]
    
    # 选择语音识别模型的类型
    model_size = ["tiny","base","small","medium","large"][2]
    model = whisper.load_model(model_size)
    
    # 清理目录
    shutil.rmtree("input/separate")
    shutil.rmtree("input/split")
    # 人声乐器分离
    spleeter_audio()
    
    # 声音根据停顿切段
    input_directory = "input/separate"
    output_directory = "input/split"
    split_audio(input_directory, output_directory)
    
    # 语音转文字
    input_directory = "input/split"
    output_directory = "input/split"
    transcribe_audio_to_text(input_directory, output_directory)
