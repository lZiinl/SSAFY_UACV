package uacv.backend.hardware.dto;

import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
public class StreamRequest {
    private String inputUrl;// RTSP 입력 스트림 URL
    private String outputName;// 생성할 HLS 스트림의 이름
}
