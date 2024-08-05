package uacv.backend.hardware.service;

import org.springframework.stereotype.Service;
import uacv.backend.stream.StreamInfo;

@Service
public class StreamService {
    private final String STREAM_URL = "rtsp://<address>:8554/live";

    public StreamInfo getStreamInfo(String streamName) {
        return new StreamInfo(STREAM_URL, streamName);
    }
}
