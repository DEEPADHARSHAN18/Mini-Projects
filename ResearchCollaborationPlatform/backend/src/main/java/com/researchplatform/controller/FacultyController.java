package com.researchplatform.controller;
import com.researchplatform.entity.*;
import com.researchplatform.repository.*;
import com.researchplatform.security.UserDetailsImpl;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.web.bind.annotation.*;
import java.util.*;

@RestController
@RequestMapping("/api")
public class FacultyController {

    @Autowired FacultyRepository facultyRepository;
    @Autowired PublicationRepository publicationRepository;
    @Autowired CollaborationRepository collaborationRepository;
    @Autowired ProjectRepository projectRepository;

    private UserDetailsImpl getCurrentUser() {
        return (UserDetailsImpl) SecurityContextHolder.getContext().getAuthentication().getPrincipal();
    }

    @GetMapping("/faculty/profile")
    @PreAuthorize("hasRole('FACULTY')")
    public ResponseEntity<?> getMyProfile() {
        Faculty faculty = facultyRepository.findByUserId(getCurrentUser().getId()).orElseThrow(() -> new RuntimeException("Faculty profile not found"));
        return ResponseEntity.ok(faculty);
    }

    @PutMapping("/faculty/profile")
    @PreAuthorize("hasRole('FACULTY')")
    public ResponseEntity<?> updateMyProfile(@RequestBody Faculty facultyDetails) {
        Faculty faculty = facultyRepository.findByUserId(getCurrentUser().getId()).orElseThrow(() -> new RuntimeException("Faculty profile not found"));
        faculty.setDepartment(facultyDetails.getDepartment());
        faculty.setExpertise(facultyDetails.getExpertise());
        faculty.setResearchInterests(facultyDetails.getResearchInterests());
        faculty.setAvailability(facultyDetails.getAvailability());
        return ResponseEntity.ok(facultyRepository.save(faculty));
    }

    @GetMapping("/faculty/publications")
    @PreAuthorize("hasRole('FACULTY')")
    public ResponseEntity<?> getMyPublications() {
        Faculty faculty = facultyRepository.findByUserId(getCurrentUser().getId()).orElseThrow();
        return ResponseEntity.ok(publicationRepository.findByFacultyId(faculty.getFacultyId()));
    }

    @PostMapping("/faculty/publications")
    @PreAuthorize("hasRole('FACULTY')")
    public ResponseEntity<?> createPublication(@RequestBody Publication publication) {
        Faculty faculty = facultyRepository.findByUserId(getCurrentUser().getId()).orElseThrow();
        publication.setFacultyId(faculty.getFacultyId());
        return ResponseEntity.ok(publicationRepository.save(publication));
    }

    @PutMapping("/faculty/publications/{id}")
    @PreAuthorize("hasRole('FACULTY')")
    public ResponseEntity<?> updatePublication(@PathVariable Integer id, @RequestBody Publication details) {
        Publication pub = publicationRepository.findById(id).orElseThrow();
        Faculty faculty = facultyRepository.findByUserId(getCurrentUser().getId()).orElseThrow();
        if (!pub.getFacultyId().equals(faculty.getFacultyId())) return ResponseEntity.status(403).build();
        pub.setTitle(details.getTitle());
        pub.setJournal(details.getJournal());
        pub.setYear(details.getYear());
        pub.setDomain(details.getDomain());
        pub.setKeywords(details.getKeywords());
        return ResponseEntity.ok(publicationRepository.save(pub));
    }

    @DeleteMapping("/faculty/publications/{id}")
    @PreAuthorize("hasRole('FACULTY')")
    public ResponseEntity<?> deletePublication(@PathVariable Integer id) {
        Publication pub = publicationRepository.findById(id).orElseThrow();
        Faculty faculty = facultyRepository.findByUserId(getCurrentUser().getId()).orElseThrow();
        if (!pub.getFacultyId().equals(faculty.getFacultyId())) return ResponseEntity.status(403).build();
        publicationRepository.delete(pub);
        return ResponseEntity.ok().build();
    }
    
    @GetMapping("/faculty/dashboard")
    @PreAuthorize("hasRole('FACULTY')")
    public ResponseEntity<?> getDashboard() {
        Faculty faculty = facultyRepository.findByUserId(getCurrentUser().getId()).orElseThrow();
        List<Publication> publications = publicationRepository.findByFacultyId(faculty.getFacultyId());
        List<Collaboration> collaborations = collaborationRepository.findByFacultyId(faculty.getFacultyId());
        Map<String, Object> stats = new HashMap<>();
        stats.put("totalPublications", publications.size());
        stats.put("pendingRequests", collaborations.stream().filter(c -> "PENDING".equals(c.getStatus())).count());
        stats.put("activeCollaborations", collaborations.stream().filter(c -> "ACCEPTED".equals(c.getStatus())).count());
        
        Map<String, Long> pubByYear = new HashMap<>();
        Map<String, Long> pubByDomain = new HashMap<>();
        for (Publication p : publications) {
            String year = p.getYear() != null ? p.getYear().toString() : "Unknown";
            String domain = p.getDomain() != null ? p.getDomain() : "Unknown";
            pubByYear.put(year, pubByYear.getOrDefault(year, 0L) + 1);
            pubByDomain.put(domain, pubByDomain.getOrDefault(domain, 0L) + 1);
        }
        stats.put("publicationsByYear", pubByYear);
        stats.put("publicationsByDomain", pubByDomain);
        
        stats.put("recentPublications", publications.stream().sorted(Comparator.comparing(Publication::getPublicationId).reversed()).limit(5).toList());
        
        return ResponseEntity.ok(stats);
    }
}
