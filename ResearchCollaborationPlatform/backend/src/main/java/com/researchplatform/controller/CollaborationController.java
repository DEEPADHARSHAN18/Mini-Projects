package com.researchplatform.controller;
import com.researchplatform.entity.*;
import com.researchplatform.repository.*;
import com.researchplatform.security.UserDetailsImpl;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.transaction.annotation.Transactional;
import org.springframework.web.bind.annotation.*;
import java.util.List;
import java.util.Map;
import java.util.HashMap;
import java.util.ArrayList;

@RestController
@RequestMapping("/api")
public class CollaborationController {

    @Autowired CollaborationRepository collaborationRepository;
    @Autowired ProjectRepository projectRepository;
    @Autowired FacultyRepository facultyRepository;
    @Autowired NotificationRepository notificationRepository;
    @Autowired UserRepository userRepository;

    private UserDetailsImpl getCurrentUser() {
        return (UserDetailsImpl) SecurityContextHolder.getContext().getAuthentication().getPrincipal();
    }

    @PostMapping("/collaborations")
    @PreAuthorize("hasRole('STUDENT')")
    @Transactional
    public ResponseEntity<?> requestCollaboration(@RequestBody Map<String, Integer> request) {
        Integer projectId = request.get("projectId");
        Integer facultyId = request.get("facultyId");
        Project project = projectRepository.findById(projectId).orElseThrow();
        if (!project.getStudentId().equals(getCurrentUser().getId())) return ResponseEntity.status(403).build();
        
        // Prevent duplicate
        if (collaborationRepository.findByProjectIdAndFacultyIdAndStudentId(projectId, facultyId, project.getStudentId()).isPresent()) {
            return ResponseEntity.badRequest().body(Map.of("message", "Collaboration request already exists."));
        }

        Collaboration col = new Collaboration();
        col.setProjectId(projectId);
        col.setFacultyId(facultyId);
        col.setStudentId(project.getStudentId());
        col.setStatus("PENDING");
        collaborationRepository.save(col);

        Faculty faculty = facultyRepository.findById(facultyId).orElseThrow();
        Notification notif = new Notification();
        notif.setUserId(faculty.getUserId());
        notif.setMessage("New collaboration request received for project: " + project.getTitle());
        notif.setStatus("UNREAD");
        notificationRepository.save(notif);

        return ResponseEntity.ok(col);
    }

    @GetMapping("/collaborations/my")
    @PreAuthorize("hasRole('STUDENT') or hasRole('FACULTY')")
    public ResponseEntity<?> getMyCollaborations() {
        UserDetailsImpl user = getCurrentUser();
        if (user.getRole().equals("STUDENT")) {
            return ResponseEntity.ok(collaborationRepository.findByStudentId(user.getId()));
        } else if (user.getRole().equals("FACULTY")) {
            Faculty faculty = facultyRepository.findByUserId(user.getId()).orElseThrow();
            return ResponseEntity.ok(collaborationRepository.findByFacultyId(faculty.getFacultyId()));
        }
        return ResponseEntity.badRequest().build();
    }

    @GetMapping("/faculty/collaboration-requests")
    @PreAuthorize("hasRole('FACULTY')")
    public ResponseEntity<?> getCollaborationRequests() {
        Faculty faculty = facultyRepository.findByUserId(getCurrentUser().getId()).orElseThrow();
        List<Collaboration> pending = collaborationRepository.findByFacultyId(faculty.getFacultyId());
        
        List<Map<String, Object>> response = new ArrayList<>();
        for (Collaboration c : pending) {
            Project p = projectRepository.findById(c.getProjectId()).orElse(null);
            User s = p != null ? userRepository.findById(p.getStudentId()).orElse(null) : null;
            
            Map<String, Object> map = new HashMap<>();
            map.put("collaborationId", c.getCollaborationId());
            map.put("projectId", c.getProjectId());
            map.put("studentId", c.getStudentId());
            map.put("status", c.getStatus());
            map.put("createdAt", c.getCreatedAt());
            if (p != null) {
                map.put("projectTitle", p.getTitle());
                map.put("projectDomain", p.getDomain());
                map.put("projectDescription", p.getDescription());
            }
            if (s != null) {
                map.put("studentName", s.getName());
                map.put("studentEmail", s.getEmail());
            }
            response.add(map);
        }
        return ResponseEntity.ok(response);
    }

    @PutMapping("/collaborations/{id}/accept")
    @PreAuthorize("hasRole('FACULTY')")
    @Transactional
    public ResponseEntity<?> acceptCollaboration(@PathVariable Integer id) {
        Collaboration col = collaborationRepository.findById(id).orElseThrow();
        Faculty faculty = facultyRepository.findByUserId(getCurrentUser().getId()).orElseThrow();
        if (!col.getFacultyId().equals(faculty.getFacultyId())) return ResponseEntity.status(403).build();
        
        if (!"PENDING".equals(col.getStatus())) {
            return ResponseEntity.badRequest().body(Map.of("message", "Only pending requests can be accepted."));
        }
        
        col.setStatus("ACCEPTED");
        collaborationRepository.save(col);

        Project project = projectRepository.findById(col.getProjectId()).orElseThrow();
        Notification notif = new Notification();
        notif.setUserId(project.getStudentId());
        notif.setMessage("Your collaboration request for project: " + project.getTitle() + " has been accepted.");
        notif.setStatus("UNREAD");
        notificationRepository.save(notif);

        return ResponseEntity.ok(col);
    }

    @PutMapping("/collaborations/{id}/reject")
    @PreAuthorize("hasRole('FACULTY')")
    @Transactional
    public ResponseEntity<?> rejectCollaboration(@PathVariable Integer id) {
        Collaboration col = collaborationRepository.findById(id).orElseThrow();
        Faculty faculty = facultyRepository.findByUserId(getCurrentUser().getId()).orElseThrow();
        if (!col.getFacultyId().equals(faculty.getFacultyId())) return ResponseEntity.status(403).build();
        
        if (!"PENDING".equals(col.getStatus())) {
            return ResponseEntity.badRequest().body(Map.of("message", "Only pending requests can be rejected."));
        }
        
        col.setStatus("REJECTED");
        collaborationRepository.save(col);

        Project project = projectRepository.findById(col.getProjectId()).orElseThrow();
        Notification notif = new Notification();
        notif.setUserId(project.getStudentId());
        notif.setMessage("Your collaboration request for project: " + project.getTitle() + " has been rejected.");
        notif.setStatus("UNREAD");
        notificationRepository.save(notif);

        return ResponseEntity.ok(col);
    }
}
