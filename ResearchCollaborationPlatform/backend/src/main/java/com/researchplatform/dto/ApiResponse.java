package com.researchplatform.dto;
import java.time.LocalDateTime;
public class ApiResponse {
    private boolean success;
    private String message;
    private LocalDateTime timestamp = LocalDateTime.now();

    public ApiResponse(boolean success, String message) {
        this.success = success;
        this.message = message;
    }
    public boolean isSuccess() { return success; }
    public String getMessage() { return message; }
    public LocalDateTime getTimestamp() { return timestamp; }
}
