package uacv.backend.stream;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.Optional;

// JpaRepository를 상속받아 기본적인 CRUD 연산 메서드를 자동으로 제공받음
@Repository
public interface StreamInfoRepository extends JpaRepository<StreamInfo, Long> {
    // 스트림 이름으로 StreamInfo를 조회하는 메서드
    // 메서드 이름 규칙에 따라 JPA가 자동으로 쿼리를 생성함
    Optional<StreamInfo> findByStreamName(String streamName);
}
