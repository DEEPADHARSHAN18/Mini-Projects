package com.researchplatform.entity;
import jakarta.persistence.*;
import java.sql.Timestamp;
import org.hibernate.annotations.CreationTimestamp;

@Entity
@Table(name = "collaborations")
public class Collaboration {
    @Id @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Integer collaborationId;
    @Column(name = "project_id")
    private Integer projectId;
    @Column(name = "faculty_id")
    private Integer facultyId;
    @Column(name = "student_id")
    private Integer studentId;
    private String status;
    @CreationTimestamp
    private Timestamp createdAt;

    public Collaboration() {}

    public Integer getCollaborationId() { return collaborationId; }
    public void setCollaborationId(Integer collaborationId) { this.collaborationId = collaborationId; }
    public Integer getProjectId() { return projectId; }
    public void setProjectId(Integer projectId) { this.projectId = projectId; }
    public Integer getFacultyId() { return facultyId; }
    public void setFacultyId(Integer facultyId) { this.facultyId = facultyId; }
    public Integer getStudentId() { return studentId; }
    public void setStudentId(Integer studentId) { this.studentId = studentId; }
    public String getStatus() { return status; }
    public void setStatus(String status) { this.status = status; }
    public Timestamp getCreatedAt() { return createdAt; }
    public void setCreatedAt(Timestamp createdAt) { this.createdAt = createdAt; }
}
