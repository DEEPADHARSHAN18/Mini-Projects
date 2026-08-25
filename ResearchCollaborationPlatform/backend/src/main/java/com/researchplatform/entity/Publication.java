package com.researchplatform.entity;
import jakarta.persistence.*;

@Entity
@Table(name = "publications")
public class Publication {
    @Id @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Integer publicationId;
    private String title;
    private String journal;
    @Column(name="pub_year") // renaming it just in case 'year' is reserved, but assuming existing schema is 'year'
    private Integer year;
    private String domain;
    private String keywords;
    @Column(name = "faculty_id")
    private Integer facultyId;

    public Publication() {}

    public Integer getPublicationId() { return publicationId; }
    public void setPublicationId(Integer publicationId) { this.publicationId = publicationId; }
    public String getTitle() { return title; }
    public void setTitle(String title) { this.title = title; }
    public String getJournal() { return journal; }
    public void setJournal(String journal) { this.journal = journal; }
    public Integer getYear() { return year; }
    public void setYear(Integer year) { this.year = year; }
    public String getDomain() { return domain; }
    public void setDomain(String domain) { this.domain = domain; }
    public String getKeywords() { return keywords; }
    public void setKeywords(String keywords) { this.keywords = keywords; }
    public Integer getFacultyId() { return facultyId; }
    public void setFacultyId(Integer facultyId) { this.facultyId = facultyId; }
}
