package com.researchplatform.controller;
import com.researchplatform.entity.Notification;
import com.researchplatform.repository.NotificationRepository;
import com.researchplatform.security.UserDetailsImpl;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.web.bind.annotation.*;
import java.util.List;
import java.util.Map;

@RestController
@RequestMapping("/api/notifications")
public class NotificationController {

    @Autowired NotificationRepository notificationRepository;

    private UserDetailsImpl getCurrentUser() {
        return (UserDetailsImpl) SecurityContextHolder.getContext().getAuthentication().getPrincipal();
    }

    @GetMapping
    public ResponseEntity<?> getNotifications() {
        return ResponseEntity.ok(notificationRepository.findByUserIdOrderByCreatedAtDesc(getCurrentUser().getId()));
    }

    @GetMapping("/unread-count")
    public ResponseEntity<?> getUnreadCount() {
        int count = notificationRepository.countByUserIdAndStatus(getCurrentUser().getId(), "UNREAD");
        return ResponseEntity.ok(Map.of("count", count));
    }

    @PutMapping("/{id}/read")
    public ResponseEntity<?> markAsRead(@PathVariable Integer id) {
        Notification notif = notificationRepository.findById(id).orElseThrow();
        if (!notif.getUserId().equals(getCurrentUser().getId())) return ResponseEntity.status(403).build();
        notif.setStatus("READ");
        return ResponseEntity.ok(notificationRepository.save(notif));
    }

    @PutMapping("/read-all")
    public ResponseEntity<?> markAllAsRead() {
        List<Notification> notifs = notificationRepository.findByUserIdOrderByCreatedAtDesc(getCurrentUser().getId());
        for (Notification n : notifs) {
            if ("UNREAD".equals(n.getStatus())) {
                n.setStatus("READ");
                notificationRepository.save(n);
            }
        }
        return ResponseEntity.ok().build();
    }
}
