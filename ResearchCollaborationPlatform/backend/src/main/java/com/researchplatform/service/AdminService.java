package com.researchplatform.service;

import com.researchplatform.dto.AdminDashboardDTO;
import com.researchplatform.dto.AdminAnalyticsDTO;
import com.researchplatform.dto.UserDTO;
import com.researchplatform.entity.User;
import com.researchplatform.entity.Collaboration;
import com.researchplatform.entity.Project;
import com.researchplatform.entity.Publication;
import com.researchplatform.repository.*;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;
import org.springframework.dao.DataIntegrityViolationException;

import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;
import java.util.Calendar;
import java.util.Collections;

@Service
public class AdminService {

    @Autowired private UserRepository userRepository;
    @Autowired private FacultyRepository facultyRepository;
    @Autowired private ProjectRepository projectRepository;
    @Autowired private PublicationRepository publicationRepository;
    @Autowired private CollaborationRepository collaborationRepository;
    @Autowired private PasswordEncoder passwordEncoder;

    public AdminDashboardDTO getDashboardStats() {
        AdminDashboardDTO dto = new AdminDashboardDTO();
        dto.setTotalUsers(userRepository.count());
        dto.setTotalFaculty(facultyRepository.count());
        dto.setTotalStudents(userRepository.findByRole("STUDENT").size());
        dto.setTotalAdmins(userRepository.findByRole("ADMIN").size());
        dto.setTotalProjects(projectRepository.count());
        dto.setTotalPublications(publicationRepository.count());

        List<Collaboration> collaborations = collaborationRepository.findAll();
        dto.setPendingCollaborations(collaborations.stream().filter(c -> "PENDING".equalsIgnoreCase(c.getStatus())).count());
        dto.setAcceptedCollaborations(collaborations.stream().filter(c -> "ACCEPTED".equalsIgnoreCase(c.getStatus())).count());
        dto.setRejectedCollaborations(collaborations.stream().filter(c -> "REJECTED".equalsIgnoreCase(c.getStatus())).count());
        return dto;
    }

    public AdminAnalyticsDTO getAnalytics() {
        AdminAnalyticsDTO dto = new AdminAnalyticsDTO();

        // User Distribution
        Map<String, Long> userDist = new HashMap<>();
        userDist.put("Students", (long) userRepository.findByRole("STUDENT").size());
        userDist.put("Faculty", (long) userRepository.findByRole("FACULTY").size());
        userDist.put("Admins", (long) userRepository.findByRole("ADMIN").size());
        dto.setUserDistribution(userDist);

        // Collaboration Status
        Map<String, Long> collabStatus = new HashMap<>();
        List<Collaboration> collabs = collaborationRepository.findAll();
        collabStatus.put("Pending", collabs.stream().filter(c -> "PENDING".equalsIgnoreCase(c.getStatus())).count());
        collabStatus.put("Accepted", collabs.stream().filter(c -> "ACCEPTED".equalsIgnoreCase(c.getStatus())).count());
        collabStatus.put("Rejected", collabs.stream().filter(c -> "REJECTED".equalsIgnoreCase(c.getStatus())).count());
        dto.setCollaborationStatus(collabStatus);

        // Publications by Year
        List<Publication> publications = publicationRepository.findAll();
        Map<Integer, Long> pubCountByYear = publications.stream()
                .filter(p -> p.getYear() != null)
                .collect(Collectors.groupingBy(Publication::getYear, Collectors.counting()));
        List<Map<String, Object>> pubByYearList = pubCountByYear.entrySet().stream()
                .map(e -> {
                    Map<String, Object> map = new HashMap<>();
                    map.put("year", e.getKey().toString());
                    map.put("count", e.getValue());
                    return map;
                })
                .sorted((m1, m2) -> ((String) m1.get("year")).compareTo((String) m2.get("year")))
                .collect(Collectors.toList());
        dto.setPublicationsByYear(pubByYearList);

        // Projects by Domain
        List<Project> projects = projectRepository.findAll();
        Map<String, Long> projCountByDomain = projects.stream()
                .filter(p -> p.getDomain() != null)
                .collect(Collectors.groupingBy(Project::getDomain, Collectors.counting()));
        List<Map<String, Object>> projByDomainList = projCountByDomain.entrySet().stream()
                .map(e -> {
                    Map<String, Object> map = new HashMap<>();
                    map.put("domain", e.getKey());
                    map.put("count", e.getValue());
                    return map;
                })
                .collect(Collectors.toList());
        dto.setProjectsByDomain(projByDomainList);

        return dto;
    }

    public User createUser(UserDTO dto) {
        if (userRepository.findByEmail(dto.getEmail()).isPresent()) {
            throw new IllegalArgumentException("Email already exists.");
        }
        User user = new User();
        user.setName(dto.getName());
        user.setEmail(dto.getEmail());
        user.setPassword(passwordEncoder.encode(dto.getPassword()));
        user.setRole(dto.getRole().toUpperCase());
        return userRepository.save(user);
    }

    public User updateUser(Integer id, UserDTO dto) {
        User user = userRepository.findById(id).orElseThrow(() -> new IllegalArgumentException("User not found"));
        user.setName(dto.getName());
        user.setRole(dto.getRole().toUpperCase());
        
        // Ensure email isn't conflicting if changed
        if (!user.getEmail().equalsIgnoreCase(dto.getEmail())) {
            if (userRepository.findByEmail(dto.getEmail()).isPresent()) {
                throw new IllegalArgumentException("Email already exists.");
            }
            user.setEmail(dto.getEmail());
        }

        if (dto.getPassword() != null && !dto.getPassword().trim().isEmpty()) {
            user.setPassword(passwordEncoder.encode(dto.getPassword()));
        }
        return userRepository.save(user);
    }

    public void deleteUser(Integer id) {
        User user = userRepository.findById(id).orElseThrow(() -> new IllegalArgumentException("User not found"));
        try {
            userRepository.delete(user);
        } catch (DataIntegrityViolationException e) {
            throw new IllegalStateException("Cannot delete user because they have associated research records or collaborations.");
        }
    }
}
