package uacv.backend.hardware.domain;

public class StreamInfo {
    // private String camera1Url;
    // private String camera2Url;
    private String camera1Url = "rtsp://192.168.100.251:5000/cam1";
    private String camera2Url = "rtsp://192.168.100.251:5001/cam2";

    // Getters and setters
    public String getCamera1Url() {
        return camera1Url;
    }

    public void setCamera1Url(String camera1Url) {
        this.camera1Url = camera1Url;
    }

    public String getCamera2Url() {
        return camera2Url;
    }

    public void setCamera2Url(String camera2Url) {
        this.camera2Url = camera2Url;
    }
}