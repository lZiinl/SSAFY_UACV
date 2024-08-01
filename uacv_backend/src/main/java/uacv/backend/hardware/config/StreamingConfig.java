package uacv.backend.hardware.config;

import org.springframework.boot.context.properties.ConfigurationProperties;
import org.springframework.context.annotation.Configuration;

@Configuration
@ConfigurationProperties(prefix = "streaming")
public class StreamingConfig {
    private String outputPath;
    private Hls hls = new Hls();

    public String getOutputPath() {
        return outputPath;
    }

    public void setOutputPath(String outputPath) {
        this.outputPath = outputPath;
    }

    public Hls getHls() {
        return hls;
    }

    public void setHls(Hls hls) {
        this.hls = hls;
    }

    public static class Hls {
        private int segmentDuration;
        private int playlistSize;

        public int getSegmentDuration() {
            return segmentDuration;
        }

        public void setSegmentDuration(int segmentDuration) {
            this.segmentDuration = segmentDuration;
        }

        public int getPlaylistSize() {
            return playlistSize;
        }

        public void setPlaylistSize(int playlistSize) {
            this.playlistSize = playlistSize;
        }
    }
}
