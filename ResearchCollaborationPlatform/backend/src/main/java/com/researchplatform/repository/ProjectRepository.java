package com.researchplatform.repository;
import com.researchplatform.entity.Project;
import org.springframework.data.jpa.repository.JpaRepository;
import java.util.List;

public interface ProjectRepository extends JpaRepository<Project, Integer> {
    List<Project> findByStudentId(Integer studentId);
}
