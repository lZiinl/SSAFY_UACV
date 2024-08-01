package uacv.backend.hardware.service;

import org.springframework.stereotype.Service;

import java.io.IOException;

@Service
public class StreamConversionService {
    private Process ffmpegProcess;

    public void startConversion(String rtspUrl, String outputPath) throws IOException {
        String[] command = {
                "ffmpeg",
                "-i", rtspUrl,
                "-c:v", "libx264",
                "-c:a", "aac",
                "-f", "hls",
                "-hls_time", "2",
                "-hls_list_size", "3",
                "-hls_flags", "delete_segments",
                outputPath
        };
        ffmpegProcess = new ProcessBuilder(command).start();
    }

    public void stopConversion() {
        if (ffmpegProcess != null) {
            ffmpegProcess.destroy();
        }
    }
}
