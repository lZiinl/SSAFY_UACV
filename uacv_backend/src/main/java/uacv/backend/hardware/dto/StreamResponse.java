package uacv.backend.hardware.dto;

import lombok.AllArgsConstructor;
import lombok.Getter;

@Getter
@AllArgsConstructor
public class StreamResponse {
    private String streamUrl; // HLS 스트림 url
    private String message; // 응답 메시지
}
