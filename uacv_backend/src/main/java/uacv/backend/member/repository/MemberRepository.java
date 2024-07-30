package uacv.backend.member.repository;

import org.springframework.data.jpa.repository.JpaRepository;

import uacv.backend.member.domain.Member;

import java.util.Optional;

public interface MemberRepository extends JpaRepository<Member, Long> {
    Optional<Member> findByUsername(String username);
}
