package com.researchplatform.repository;
import com.researchplatform.entity.Publication;
import org.springframework.data.jpa.repository.JpaRepository;
import java.util.List;

public interface PublicationRepository extends JpaRepository<Publication, Integer> {
    List<Publication> findByFacultyId(Integer facultyId);
}
