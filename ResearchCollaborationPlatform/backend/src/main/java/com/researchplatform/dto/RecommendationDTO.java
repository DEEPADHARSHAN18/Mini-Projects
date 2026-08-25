package com.researchplatform.dto;
import com.researchplatform.entity.Faculty;
import com.researchplatform.entity.CompatibilityScore;

public class RecommendationDTO {
    private Faculty faculty;
    private String facultyName;
    private CompatibilityScore score;
    private String explanation;
    private String collaborationStatus;

    public RecommendationDTO(Faculty faculty, String facultyName, CompatibilityScore score, String explanation, String collaborationStatus) {
        this.faculty = faculty;
        this.facultyName = facultyName;
        this.score = score;
        this.explanation = explanation;
        this.collaborationStatus = collaborationStatus;
    }
    public Faculty getFaculty() { return faculty; }
    public String getFacultyName() { return facultyName; }
    public CompatibilityScore getScore() { return score; }
    public String getExplanation() { return explanation; }
    public String getCollaborationStatus() { return collaborationStatus; }
}
