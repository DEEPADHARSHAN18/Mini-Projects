package com.researchplatform.dto;

public class AdminDashboardDTO {
    private long totalUsers;
    private long totalStudents;
    private long totalFaculty;
    private long totalAdmins;
    private long totalProjects;
    private long totalPublications;
    private long pendingCollaborations;
    private long acceptedCollaborations;
    private long rejectedCollaborations;

    // Getters and Setters
    public long getTotalUsers() { return totalUsers; }
    public void setTotalUsers(long totalUsers) { this.totalUsers = totalUsers; }
    public long getTotalStudents() { return totalStudents; }
    public void setTotalStudents(long totalStudents) { this.totalStudents = totalStudents; }
    public long getTotalFaculty() { return totalFaculty; }
    public void setTotalFaculty(long totalFaculty) { this.totalFaculty = totalFaculty; }
    public long getTotalAdmins() { return totalAdmins; }
    public void setTotalAdmins(long totalAdmins) { this.totalAdmins = totalAdmins; }
    public long getTotalProjects() { return totalProjects; }
    public void setTotalProjects(long totalProjects) { this.totalProjects = totalProjects; }
    public long getTotalPublications() { return totalPublications; }
    public void setTotalPublications(long totalPublications) { this.totalPublications = totalPublications; }
    public long getPendingCollaborations() { return pendingCollaborations; }
    public void setPendingCollaborations(long pendingCollaborations) { this.pendingCollaborations = pendingCollaborations; }
    public long getAcceptedCollaborations() { return acceptedCollaborations; }
    public void setAcceptedCollaborations(long acceptedCollaborations) { this.acceptedCollaborations = acceptedCollaborations; }
    public long getRejectedCollaborations() { return rejectedCollaborations; }
    public void setRejectedCollaborations(long rejectedCollaborations) { this.rejectedCollaborations = rejectedCollaborations; }
}
