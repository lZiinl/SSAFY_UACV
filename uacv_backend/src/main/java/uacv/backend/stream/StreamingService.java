package uacv.backend.stream;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;

import java.io.IOException;

//@RequiredArgsConstructor
@Service
public class StreamingService {
    @Value("${ffmpeg.path}")
    private String ffmpegPath; // FFmpeg 실행 파일 경로

    @Value("${streaming.output-path}")
    private String outputPath; // HLS 스트림 파일 저장될 경로

    @Value("${streaming.hls.segment-duration}")
    private int segmentDuration; // 각 HLS 세그먼트의 길이(초)

    @Value("${streaming.hls.playlist-size}")
    private int playlistSize; // 플레이리스트에 유지할 세그먼트의 수

    @Autowired
    private StreamInfoRepository streamInfoRepository; // StreamInfo 엔티티를 관리하는 리포지토리

    /**
     * RTSP 스트림을 HLS로 변환하고 스트리밍을 시작합니다.
     *
     * @param inputUrl   RTSP 입력 스트림 URL
     * @param outputName 출력 스트림의 이름
     * @return 생성된 HLS 스트림의 상대 경로
     */
    public String startStreaming(String inputUrl, String outputName) {
        // 출력 파일의 전체 경로(.m3u8 파일)
        String outputUrl = outputPath + "/" + outputName + ".m3u8";

        // FFmpeg 명령어 구성
        String command = String.format("%s -i %s -c:v libx264 -c:a aac -f hls -hls_time %d -hls_list_size %d %s",
                ffmpegPath, inputUrl, segmentDuration, playlistSize, outputUrl);

        try {
            // FFmpeg 프로세스 실행
            Process process = Runtime.getRuntime().exec(command);
            // TODO: 프로세스 관리 로직 추가 (로깅, 오류 처리 등)
        } catch (IOException e) {
            // 예외 발생 시 RuntimeException으로 래핑하여 던짐
            throw new RuntimeException("스트리밍 시작 중 오류 발생", e);
        }

        String relativePath = "hls/" + outputName + ".m3u8";

        //StreamINfo 객체 생성 및 저장
        StreamInfo streamInfo = new StreamInfo(relativePath, outputName);
        streamInfoRepository.save(streamInfo);
        // Inferred type 'S' for type parameter 'S' is not within its bound; should implement 'javax.xml.crypto.dsig.SignedInfo'
        // >>> there might be a problem with the generics in your StreamInfoRepository. This typically happens when there is a type mismatch or an incorrect type parameter is inferred.
        return relativePath;
    }

    /**
     * 스트림 이름으로 StreamInfo를 조회합니다.
     *
     * @param streamName 조회할 스트림의 이름
     * @return 조회된 StreamInfo 객체
     * @throws RuntimeException 스트림을 찾을 수 없을 경우
     */
    public StreamInfo getStreamInfo(String streamName) {
        return streamInfoRepository.findByStreamName(streamName)
                .orElseThrow(() -> new RuntimeException("Stream not found"));
    }
    // TODO: 스트리밍 중지, 상태 확인 등의 추가 메서드 구현
}
