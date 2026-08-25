package com.researchplatform.entity;
import jakarta.persistence.*;
import java.math.BigDecimal;

@Entity
@Table(name = "compatibility_scores")
public class CompatibilityScore {
    @Id @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Integer scoreId;
    @Column(name = "project_id")
    private Integer projectId;
    @Column(name = "faculty_id")
    private Integer facultyId;
    private BigDecimal domainScore;
    private BigDecimal keywordScore;
    private BigDecimal expertiseScore;
    private BigDecimal publicationScore;
    private BigDecimal availabilityScore;
    private BigDecimal totalScore;

    public CompatibilityScore() {}

    public Integer getScoreId() { return scoreId; }
    public void setScoreId(Integer scoreId) { this.scoreId = scoreId; }
    public Integer getProjectId() { return projectId; }
    public void setProjectId(Integer projectId) { this.projectId = projectId; }
    public Integer getFacultyId() { return facultyId; }
    public void setFacultyId(Integer facultyId) { this.facultyId = facultyId; }
    public BigDecimal getDomainScore() { return domainScore; }
    public void setDomainScore(BigDecimal domainScore) { this.domainScore = domainScore; }
    public BigDecimal getKeywordScore() { return keywordScore; }
    public void setKeywordScore(BigDecimal keywordScore) { this.keywordScore = keywordScore; }
    public BigDecimal getExpertiseScore() { return expertiseScore; }
    public void setExpertiseScore(BigDecimal expertiseScore) { this.expertiseScore = expertiseScore; }
    public BigDecimal getPublicationScore() { return publicationScore; }
    public void setPublicationScore(BigDecimal publicationScore) { this.publicationScore = publicationScore; }
    public BigDecimal getAvailabilityScore() { return availabilityScore; }
    public void setAvailabilityScore(BigDecimal availabilityScore) { this.availabilityScore = availabilityScore; }
    public BigDecimal getTotalScore() { return totalScore; }
    public void setTotalScore(BigDecimal totalScore) { this.totalScore = totalScore; }
}
