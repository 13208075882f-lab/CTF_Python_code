import wave
import numpy as np
from scipy.fft import fft
from scipy.io import wavfile

WAV_FILE = "00076499.wav"
# 常见DTMF频率表（固定不用改）
DTMF_FREQS = {
    (697, 1209): '1', (697, 1336): '2', (697, 1477): '3', (697, 1633): 'A',
    (770, 1209): '4', (770, 1336): '5', (770, 1336): '5', (770, 1477): '6',
    (852, 1209): '7', (852, 1336): '8', (852, 1477): '9', (852, 1633): 'C',
    (941, 1209): '*', (941, 1336): '0', (941, 1477): '#', (941, 1633): 'D'
}

def decode_dtmf(file_path):
    # 读取音频文件
    rate, data = wavfile.read(file_path)
    # 单声道处理
    if len(data.shape) > 1:
        data = data[:, 0]
    
    # 分块参数，根据音频调整
    chunk_duration = 0.1  # 每块0.1秒
    chunk_size = int(rate * chunk_duration)
    min_amplitude = 500   # 过滤无信号噪音，根据实际情况调整
    
    digits = []
    prev_digit = None
    
    for i in range(0, len(data), chunk_size):
        chunk = data[i:i+chunk_size]
        if len(chunk) < chunk_size:
            break
        
        # 跳过噪音块
        if np.max(np.abs(chunk)) < min_amplitude:
            prev_digit = None
            continue
        
        # FFT分析频率
        yf = fft(chunk)
        xf = np.linspace(0, rate/2, len(chunk)//2)
        magnitude = 2.0 / len(chunk) * np.abs(yf[:len(chunk)//2])
        
        # 取前2个最高频率
        top_indices = np.argsort(magnitude)[-2:]
        top_freqs = xf[top_indices]
        low_freq, high_freq = sorted(top_freqs)
        
        # 匹配DTMF
        matched = None
        for (lf, hf), char in DTMF_FREQS.items():
            if abs(low_freq - lf) < 20 and abs(high_freq - hf) < 20:
                matched = char
                break
        
        if matched and matched != prev_digit:
            digits.append(matched)
            prev_digit = matched
    
    return ''.join(digits)

if __name__ == "__main__":
    result = decode_dtmf(WAV_FILE)
    print("解码结果：", result)