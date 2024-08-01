package uacv.backend.hardware.service;


import org.springframework.core.io.Resource;

import uacv.backend.hardware.domain.StreamInfo;

import java.io.IOException;

public interface StreamService {
    void startStream(StreamInfo streamInfo) throws IOException;
    void stopStreams();
    Resource getPlaylist(String cameraId);
    Resource getSegment(String cameraId, String segment);
}