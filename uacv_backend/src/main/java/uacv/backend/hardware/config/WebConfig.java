package uacv.backend.hardware.config;

import org.springframework.context.annotation.Configuration;
import org.springframework.web.servlet.config.annotation.CorsRegistry;
import org.springframework.web.servlet.config.annotation.WebMvcConfigurer;

@Configuration
public class WebConfig implements WebMvcConfigurer {
    @Override
    public void addCorsMappings(CorsRegistry registry) {
        registry.addMapping("/api/**")
                .allowedOrigins("http://localhost:8080") // vue 개발 서버 주소
                .allowedMethods("GET", "POST", "PUT", "DELETE")
                .allowedHeaders("*");

        // HLS 스트림 파일에 대한 CORS 설정
        registry.addMapping("/hls/**")
                .allowedOrigins("*")
                .allowedMethods("GET", "HEAD")
                .allowedHeaders("*");
    }

}
