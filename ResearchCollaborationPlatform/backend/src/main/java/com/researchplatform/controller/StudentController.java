package com.researchplatform.controller;
import com.researchplatform.entity.*;
import com.researchplatform.repository.*;
import com.researchplatform.security.UserDetailsImpl;
import com.researchplatform.service.CompatibilityScoringService;
import com.researchplatform.dto.RecommendationDTO;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.web.bind.annotation.*;
import java.util.*;

@RestController
@RequestMapping("/api")
public class StudentController {

    @Autowired ProjectRepository projectRepository;
    @Autowired FacultyRepository facultyRepository;
    @Autowired UserRepository userRepository;
    @Autowired PublicationRepository publicationRepository;
    @Autowired CompatibilityScoreRepository scoreRepository;
    @Autowired CompatibilityScoringService scoringService;
    @Autowired CollaborationRepository collaborationRepository;

    private UserDetailsImpl getCurrentUser() {
        return (UserDetailsImpl) SecurityContextHolder.getContext().getAuthentication().getPrincipal();
    }

    @GetMapping("/student/dashboard")
    @PreAuthorize("hasRole('STUDENT')")
    public ResponseEntity<?> getDashboard() {
        Integer studentId = getCurrentUser().getId();
        List<Project> projects = projectRepository.findByStudentId(studentId);
        List<Collaboration> collaborations = collaborationRepository.findByStudentId(studentId);
        Map<String, Object> stats = new HashMap<>();
        stats.put("totalProjects", projects.size());
        stats.put("activeProjects", projects.stream().filter(p -> "IN_PROGRESS".equals(p.getStatus()) || "OPEN".equals(p.getStatus())).count());
        stats.put("completedProjects", projects.stream().filter(p -> "COMPLETED".equals(p.getStatus())).count());
        stats.put("totalCollaborations", collaborations.size());
        stats.put("pendingCollaborations", collaborations.stream().filter(c -> "PENDING".equals(c.getStatus())).count());
        stats.put("acceptedCollaborations", collaborations.stream().filter(c -> "ACCEPTED".equals(c.getStatus())).count());
        stats.put("rejectedCollaborations", collaborations.stream().filter(c -> "REJECTED".equals(c.getStatus())).count());
        stats.put("recentProjects", projects.stream().sorted(Comparator.comparing(Project::getCreatedAt).reversed()).limit(5).toList());
        
        Map<String, Long> projectsByDomain = new HashMap<>();
        Map<String, Long> projectsByStatus = new HashMap<>();
        for (Project p : projects) {
            String domain = p.getDomain() != null ? p.getDomain() : "Unknown";
            String status = p.getStatus() != null ? p.getStatus() : "Unknown";
            projectsByDomain.put(domain, projectsByDomain.getOrDefault(domain, 0L) + 1);
            projectsByStatus.put(status, projectsByStatus.getOrDefault(status, 0L) + 1);
        }
        stats.put("projectsByDomain", projectsByDomain);
        stats.put("projectsByStatus", projectsByStatus);
        
        return ResponseEntity.ok(stats);
    }

    @GetMapping("/student/faculty/{facultyId}/publications")
    @PreAuthorize("hasRole('STUDENT')")
    public ResponseEntity<?> getFacultyPublications(@PathVariable Integer facultyId) {
        return ResponseEntity.ok(publicationRepository.findByFacultyId(facultyId));
    }

    @GetMapping("/projects/my")
    @PreAuthorize("hasRole('STUDENT')")
    public ResponseEntity<?> getMyProjects() {
        return ResponseEntity.ok(projectRepository.findByStudentId(getCurrentUser().getId()));
    }

    @PostMapping("/projects")
    @PreAuthorize("hasRole('STUDENT')")
    public ResponseEntity<?> createProject(@RequestBody Project project) {
        project.setStudentId(getCurrentUser().getId());
        project.setStatus("OPEN");
        return ResponseEntity.ok(projectRepository.save(project));
    }

    @GetMapping("/projects/{id}")
    @PreAuthorize("hasRole('STUDENT')")
    public ResponseEntity<?> getProject(@PathVariable Integer id) {
        Project project = projectRepository.findById(id).orElseThrow(() -> new RuntimeException("Project not found"));
        if (!project.getStudentId().equals(getCurrentUser().getId())) {
            return ResponseEntity.status(403).build();
        }
        return ResponseEntity.ok(project);
    }

    @PutMapping("/projects/{id}")
    @PreAuthorize("hasRole('STUDENT')")
    public ResponseEntity<?> updateProject(@PathVariable Integer id, @RequestBody Project projectDetails) {
        Project project = projectRepository.findById(id).orElseThrow(() -> new RuntimeException("Project not found"));
        if (!project.getStudentId().equals(getCurrentUser().getId())) {
            return ResponseEntity.status(403).build();
        }
        project.setTitle(projectDetails.getTitle());
        project.setDescription(projectDetails.getDescription());
        project.setDomain(projectDetails.getDomain());
        project.setKeywords(projectDetails.getKeywords());
        project.setStatus(projectDetails.getStatus());
        return ResponseEntity.ok(projectRepository.save(project));
    }

    @DeleteMapping("/projects/{id}")
    @PreAuthorize("hasRole('STUDENT')")
    public ResponseEntity<?> deleteProject(@PathVariable Integer id) {
        Project project = projectRepository.findById(id).orElseThrow(() -> new RuntimeException("Project not found"));
        if (!project.getStudentId().equals(getCurrentUser().getId())) {
            return ResponseEntity.status(403).build();
        }
        projectRepository.delete(project);
        return ResponseEntity.ok().build();
    }

    @GetMapping("/projects/{projectId}/recommendations")
    @PreAuthorize("hasRole('STUDENT')")
    public ResponseEntity<?> getRecommendations(@PathVariable Integer projectId) {
        Project project = projectRepository.findById(projectId).orElseThrow(() -> new RuntimeException("Project not found"));
        if (!project.getStudentId().equals(getCurrentUser().getId())) {
            return ResponseEntity.status(403).build();
        }
        List<RecommendationDTO> recommendations = new ArrayList<>();
        List<Faculty> allFaculty = facultyRepository.findAll();
        for (Faculty faculty : allFaculty) {
            List<Publication> publications = publicationRepository.findByFacultyId(faculty.getFacultyId());
            User facultyUser = userRepository.findById(faculty.getUserId()).orElse(null);
            if (facultyUser == null) continue;
            Optional<Collaboration> existingCollab = collaborationRepository.findByProjectIdAndFacultyIdAndStudentId(project.getProjectId(), faculty.getFacultyId(), project.getStudentId());
            String collabStatus = existingCollab.map(Collaboration::getStatus).orElse(null);
            
            CompatibilityScore score = scoringService.calculateScore(project, faculty, publications);
            String explanation = scoringService.generateExplanation(score, project, faculty, publications);
            recommendations.add(new RecommendationDTO(faculty, facultyUser.getName(), score, explanation, collabStatus));
        }
        recommendations.sort(Comparator.comparing((RecommendationDTO r) -> r.getScore().getTotalScore()).reversed());
        return ResponseEntity.ok(recommendations);
    }
}
