package uacv.backend.stream;

import com.fasterxml.jackson.annotation.JsonInclude;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import uacv.backend.hardware.dto.StreamRequest;
import uacv.backend.hardware.dto.StreamResponse;

@RestController
@RequestMapping("/api/feed")
public class StreamController {
    private final StreamingService streamingService;
//
//    @Value("${server.address}")
//    private String serverAddress;  // 서버 주소

//    @Value("${server.port}")
//    private String serverPort;  // 서버 포트

    @Autowired
    public StreamController(StreamingService streamingService) {
        this.streamingService = streamingService;
    }

    /**
     * 새로운 스트리밍을 시작하고 HLS 스트림 URL을 반환하는 엔드포인트
     * @param request 스트리밍 요청 정보를 담은 객체
     * @return HLS 스트림 URL을 포함한 응답
     */
    @PostMapping("/start")
    public ResponseEntity<StreamResponse> startStream(@RequestBody StreamRequest request) {
        System.out.println(11111);
        // 스트리밍 서비스를 통해 스트리밍 시작 및 상대 경로 받기
        String relativePath = streamingService.startStreaming(request.getInputUrl(), request.getOutputName());

        // 전체 HLS 스트림 URL 생성
        String ec2Domain = "localhost";
        String hlsUrl = String.format("http://%s:%s/%s", ec2Domain, 8080, relativePath);

        // 응답 객체 생성 및 반환
        StreamResponse response = new StreamResponse(hlsUrl, "Streaming started");
        return ResponseEntity.ok(response);
    }

    /**
     * 스트림 이름으로 스트림 정보를 조회하는 엔드포인트
     * @param streamName 조회할 스트림의 이름
     * @return 조회된 StreamInfo 객체
     */
    @GetMapping("/{streamName}")
    public ResponseEntity<StreamInfo> getStreamInfo(@PathVariable String streamName) {
        System.out.println(222222);
        StreamInfo streamInfo = streamingService.getStreamInfo(streamName);
        return ResponseEntity.ok(streamInfo);
    }
}
