package com.researchplatform.repository;
import com.researchplatform.entity.Notification;
import org.springframework.data.jpa.repository.JpaRepository;
import java.util.List;

public interface NotificationRepository extends JpaRepository<Notification, Integer> {
    List<Notification> findByUserIdOrderByCreatedAtDesc(Integer userId);
    int countByUserIdAndStatus(Integer userId, String status);
}
