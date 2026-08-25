package com.researchplatform.repository;
import com.researchplatform.entity.Collaboration;
import org.springframework.data.jpa.repository.JpaRepository;
import java.util.List;
import java.util.Optional;

public interface CollaborationRepository extends JpaRepository<Collaboration, Integer> {
    List<Collaboration> findByStudentId(Integer studentId);
    List<Collaboration> findByFacultyId(Integer facultyId);
    Optional<Collaboration> findByProjectIdAndFacultyIdAndStudentId(Integer projectId, Integer facultyId, Integer studentId);
}
