package uacv.backend.hardware.service.implement;

// import com.example.picamstreaming.model.StreamInfo;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.core.io.FileSystemResource;
import org.springframework.core.io.Resource;
import org.springframework.stereotype.Service;

import uacv.backend.hardware.config.FFmpegConfig;
import uacv.backend.hardware.config.StreamingConfig;
import uacv.backend.hardware.domain.StreamInfo;
import uacv.backend.hardware.service.StreamService;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.HashMap;
import java.util.Map;
import java.util.concurrent.CompletableFuture;

@Service
public class StreamServiceImpl implements StreamService {

    @Autowired
    private FFmpegConfig ffmpegConfig;

    @Autowired
    private StreamingConfig streamingConfig;

    private Map<String, Process> ffmpegProcesses = new HashMap<>();
    private Path streamOutputPath; // = Paths.get("/tmp/streams");

    @Override
    public void startStream(StreamInfo streamInfo) throws IOException {
        stopStreams(); // Stop any existing streams

        streamOutputPath = Paths.get(streamingConfig.getOutputPath());
        Files.createDirectories(streamOutputPath);

        startFFmpegProcess(streamInfo.getCamera1Url(), "camera1");
        startFFmpegProcess(streamInfo.getCamera2Url(), "camera2");
    }

    private void startFFmpegProcess(String rtspUrl, String cameraId) throws IOException {
        Path outputPath = streamOutputPath.resolve(cameraId);
        Files.createDirectories(outputPath);

        String[] command = {
                ffmpegConfig.getPath(),
                "-i", rtspUrl,
                "-c:v", "libx264",
                "-c:a", "aac",
                "-f", "hls",
                "-hls_time", String.valueOf(streamingConfig.getHls().getSegmentDuration()),
                "-hls_list_size", String.valueOf(streamingConfig.getHls().getPlaylistSize()),
                "-hls_flags", "delete_segments",
                outputPath.resolve("playlist.m3u8").toString()
        };

        Process process = new ProcessBuilder(command).start();
        ffmpegProcesses.put(cameraId, process);

        CompletableFuture.runAsync(() -> {
            try {
                process.waitFor();
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
        });
    }

    @Override
    public void stopStreams() {
        ffmpegProcesses.values().forEach(Process::destroyForcibly);
        ffmpegProcesses.clear();
    }

    @Override
    public Resource getPlaylist(String cameraId) {
        Path playlistPath = streamOutputPath.resolve(cameraId).resolve("playlist.m3u8");
        return new FileSystemResource(playlistPath);
    }

    @Override
    public Resource getSegment(String cameraId, String segment) {
        Path segmentPath = streamOutputPath.resolve(cameraId).resolve(segment);
        return new FileSystemResource(segmentPath);
    }
}