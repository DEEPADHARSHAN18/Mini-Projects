package com.researchplatform.dto;

import java.util.Map;
import java.util.List;

public class AdminAnalyticsDTO {
    private Map<String, Long> userDistribution;
    private Map<String, Long> collaborationStatus;
    private List<Map<String, Object>> publicationsByYear;
    private List<Map<String, Object>> projectsByDomain;

    public Map<String, Long> getUserDistribution() { return userDistribution; }
    public void setUserDistribution(Map<String, Long> userDistribution) { this.userDistribution = userDistribution; }
    public Map<String, Long> getCollaborationStatus() { return collaborationStatus; }
    public void setCollaborationStatus(Map<String, Long> collaborationStatus) { this.collaborationStatus = collaborationStatus; }
    public List<Map<String, Object>> getPublicationsByYear() { return publicationsByYear; }
    public void setPublicationsByYear(List<Map<String, Object>> publicationsByYear) { this.publicationsByYear = publicationsByYear; }
    public List<Map<String, Object>> getProjectsByDomain() { return projectsByDomain; }
    public void setProjectsByDomain(List<Map<String, Object>> projectsByDomain) { this.projectsByDomain = projectsByDomain; }
}
