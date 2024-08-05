package uacv.backend.stream;

import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

@Entity
@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
public class StreamInfo {
    @Id // PK
    @GeneratedValue(strategy = GenerationType.IDENTITY) // 일단 자동증가하게
    private Long id;

    private String streamURL;
    private String streamName;
    private String status; // 스트림 현재 상태(active, inactive,,, )

    // 생성자
    public StreamInfo(String streamURL, String streamName) {
       this.streamURL = streamURL;
       this.streamName = streamName;
       this.status = "ACTIVE"; // default
    }
}
