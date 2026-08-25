package com.researchplatform.repository;
import com.researchplatform.entity.CompatibilityScore;
import org.springframework.data.jpa.repository.JpaRepository;
import java.util.List;
import java.util.Optional;

public interface CompatibilityScoreRepository extends JpaRepository<CompatibilityScore, Integer> {
    List<CompatibilityScore> findByProjectId(Integer projectId);
    Optional<CompatibilityScore> findByProjectIdAndFacultyId(Integer projectId, Integer facultyId);
}
