package uacv.backend.hardware.api;

import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.*;
import uacv.backend.hardware.service.StreamConversionService;
import uacv.backend.member.domain.Member;
import uacv.backend.member.domain.Response;
import uacv.backend.member.dto.MemberLoginRequestDto;
import uacv.backend.member.dto.SignupDto;
import uacv.backend.member.security.jwt.TokenInfo;
import uacv.backend.member.service.MemberService;

import java.io.IOException;

@RequiredArgsConstructor
@RestController
@RequestMapping("/video")
@Slf4j
public class StreamController {
    @Autowired
    private StreamConversionService streamConversionService;

    @GetMapping("/start-stream")
    @ResponseBody
    public String startStream() throws IOException {
        streamConversionService.startConversion("rtsp://i11c102.p.ssafy.io:8554/live", "/0");
        return "Stream conversion started";
    }

    @GetMapping("/view")
    public String viewStream() {
        return "stream";
    }
}
