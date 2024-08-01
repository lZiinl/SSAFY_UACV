package uacv.backend.hardware.config;

import org.springframework.context.annotation.Configuration;
import org.springframework.boot.context.properties.ConfigurationProperties;


@Configuration
@ConfigurationProperties(prefix = "ffmpeg")
public class FFmpegConfig {
    private String path;

    public String getPath() {
        return path;
    }

    public void setPath(String path) {
        this.path = path;
}
