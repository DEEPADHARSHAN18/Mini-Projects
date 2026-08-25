package com.researchplatform.service;
import com.researchplatform.entity.CompatibilityScore;
import com.researchplatform.entity.Faculty;
import com.researchplatform.entity.Project;
import com.researchplatform.entity.Publication;
import org.springframework.stereotype.Service;
import java.math.BigDecimal;
import java.math.RoundingMode;
import java.util.Arrays;
import java.util.HashSet;
import java.util.List;
import java.util.Set;
import java.util.stream.Collectors;

@Service
public class CompatibilityScoringService {

    private static final double WEIGHT_DOMAIN = 0.25;
    private static final double WEIGHT_KEYWORD = 0.25;
    private static final double WEIGHT_EXPERTISE = 0.20;
    private static final double WEIGHT_PUBLICATION = 0.20;
    private static final double WEIGHT_AVAILABILITY = 0.10;

    public CompatibilityScore calculateScore(Project project, Faculty faculty, List<Publication> publications) {
        double domainScore = calculateDomainScore(project.getDomain(), faculty.getDepartment());
        double keywordScore = calculateKeywordScore(project.getKeywords(), faculty.getExpertise() + ", " + faculty.getResearchInterests());
        double expertiseScore = calculateExpertiseScore(project.getDomain(), project.getKeywords(), faculty.getExpertise(), faculty.getResearchInterests());
        double pubScore = calculatePublicationScore(project, publications);
        double availabilityScore = calculateAvailabilityScore(faculty.getAvailability());

        double totalScore = (domainScore * WEIGHT_DOMAIN)
                + (keywordScore * WEIGHT_KEYWORD)
                + (expertiseScore * WEIGHT_EXPERTISE)
                + (pubScore * WEIGHT_PUBLICATION)
                + (availabilityScore * WEIGHT_AVAILABILITY);

        CompatibilityScore score = new CompatibilityScore();
        score.setProjectId(project.getProjectId());
        score.setFacultyId(faculty.getFacultyId());
        score.setDomainScore(round(domainScore));
        score.setKeywordScore(round(keywordScore));
        score.setExpertiseScore(round(expertiseScore));
        score.setPublicationScore(round(pubScore));
        score.setAvailabilityScore(round(availabilityScore));
        score.setTotalScore(round(totalScore));

        return score;
    }

    public String generateExplanation(CompatibilityScore score, Project project, Faculty faculty, List<Publication> publications) {
        StringBuilder explanation = new StringBuilder();
        Set<String> projectTokens = tokenize(project.getKeywords());
        Set<String> facultyTokens = tokenize(faculty.getExpertise() + ", " + faculty.getResearchInterests());
        Set<String> overlap = new HashSet<>(projectTokens);
        overlap.retainAll(facultyTokens);

        if (!overlap.isEmpty()) {
            explanation.append("Strong keyword overlap: ").append(String.join(", ", overlap)).append("\n");
        } else {
            explanation.append("Limited keyword overlap.\n");
        }

        if (score.getExpertiseScore().doubleValue() >= 70) {
            explanation.append("Strong expertise match.\n");
        } else if (score.getExpertiseScore().doubleValue() >= 40) {
            explanation.append("Moderate expertise match.\n");
        }

        long relevantPubs = 0;
        Set<String> pTokens = tokenize(project.getKeywords());
        for (Publication pub : publications) {
            Set<String> pubTokens = tokenize(pub.getKeywords() + ", " + pub.getDomain());
            Set<String> pubOverlap = new HashSet<>(pTokens);
            pubOverlap.retainAll(pubTokens);
            if (!pubOverlap.isEmpty() || textContains(pub.getDomain(), project.getDomain())) {
                relevantPubs++;
            }
        }
        explanation.append("Relevant publications found: ").append(relevantPubs).append("\n");
        explanation.append("Availability: ").append(faculty.getAvailability() != null ? faculty.getAvailability() : "UNKNOWN");
        return explanation.toString();
    }

    private double calculateDomainScore(String projectDomain, String facultyDept) {
        if (projectDomain == null || facultyDept == null) return 0;
        String pDom = projectDomain.toLowerCase().trim();
        String fDept = facultyDept.toLowerCase().trim();
        if (pDom.equals(fDept)) return 100.0;
        if (fDept.contains(pDom) || pDom.contains(fDept)) return 75.0;
        String[] pTokens = pDom.split("\\s+");
        for (String t : pTokens) {
            if (t.length() > 3 && fDept.contains(t)) return 50.0;
        }
        return 0.0;
    }

    private double calculateKeywordScore(String projectKeywords, String facultyText) {
        if (projectKeywords == null || projectKeywords.trim().isEmpty() || facultyText == null) return 0.0;
        Set<String> pTokens = tokenize(projectKeywords);
        Set<String> fTokens = tokenize(facultyText);
        if (pTokens.isEmpty()) return 0.0;
        int matchCount = 0;
        for (String pt : pTokens) {
            if (fTokens.contains(pt)) {
                matchCount++;
            } else {
                for (String ft : fTokens) {
                    if (ft.contains(pt) || pt.contains(ft)) {
                        matchCount++;
                        break;
                    }
                }
            }
        }
        return Math.min(100.0, ((double) matchCount / pTokens.size()) * 100.0);
    }

    private double calculateExpertiseScore(String pDomain, String pKeywords, String fExpertise, String fInterests) {
        String combinedProject = (pDomain + " " + pKeywords).toLowerCase();
        String combinedFaculty = (fExpertise + " " + fInterests).toLowerCase();
        Set<String> pTokens = tokenize(combinedProject);
        Set<String> fTokens = tokenize(combinedFaculty);
        if (pTokens.isEmpty()) return 0.0;
        int matchCount = 0;
        for (String pt : pTokens) {
            if (fTokens.contains(pt)) {
                matchCount++;
            }
        }
        return Math.min(100.0, ((double) matchCount / pTokens.size()) * 100.0);
    }

    private double calculatePublicationScore(Project project, List<Publication> publications) {
        if (publications == null || publications.isEmpty()) return 0.0;
        double totalScore = 0.0;
        for (Publication pub : publications) {
            double pubScore = 0.0;
            if (textContains(pub.getDomain(), project.getDomain())) {
                pubScore += 50.0;
            }
            double kScore = calculateKeywordScore(project.getKeywords(), pub.getKeywords());
            pubScore += (kScore * 0.5);
            totalScore += pubScore;
        }
        return Math.min(100.0, totalScore);
    }

    private double calculateAvailabilityScore(String availability) {
        if (availability == null) return 0.0;
        if (availability.equalsIgnoreCase("AVAILABLE")) return 100.0;
        if (availability.equalsIgnoreCase("BUSY")) return 30.0;
        return 0.0;
    }

    private Set<String> tokenize(String text) {
        if (text == null) return new HashSet<>();
        return Arrays.stream(text.split("[,\\s]+"))
                .map(String::toLowerCase)
                .map(String::trim)
                .filter(s -> s.length() > 2)
                .collect(Collectors.toSet());
    }

    private boolean textContains(String text1, String text2) {
        if (text1 == null || text2 == null) return false;
        return text1.toLowerCase().contains(text2.toLowerCase().trim()) || text2.toLowerCase().contains(text1.toLowerCase().trim());
    }

    private BigDecimal round(double value) {
        return new BigDecimal(value).setScale(2, RoundingMode.HALF_UP);
    }
}
