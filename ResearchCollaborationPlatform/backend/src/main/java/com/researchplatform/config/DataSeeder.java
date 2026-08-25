package com.researchplatform.config;

import com.researchplatform.entity.*;
import com.researchplatform.repository.*;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.CommandLineRunner;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Component;
import java.sql.Timestamp;
import java.util.Date;
import java.util.Optional;

@Component
public class DataSeeder implements CommandLineRunner {

    @Autowired private UserRepository userRepository;
    @Autowired private FacultyRepository facultyRepository;
    @Autowired private ProjectRepository projectRepository;
    @Autowired private PublicationRepository publicationRepository;
    @Autowired private CollaborationRepository collaborationRepository;
    @Autowired private PasswordEncoder passwordEncoder;

    @Override
    public void run(String... args) throws Exception {
        System.out.println("Checking and seeding demo data...");

        // 1. Seed Faculty
        User f1 = createFacultyUser("Dr. Priya Raman", "priya.raman@research.com", "Priya@123", "Artificial Intelligence", "Machine Learning, Deep Learning, Computer Vision", "Explainable AI, Intelligent Systems");
        User f2 = createFacultyUser("Dr. Michael Chen", "michael.chen@research.com", "Michael@123", "Cybersecurity", "Network Security, Intrusion Detection", "Zero Trust, Threat Intelligence");
        User f3 = createFacultyUser("Dr. Sofia Martinez", "sofia.martinez@research.com", "Sofia@123", "Data Science", "Data Mining, Predictive Analytics", "Big Data, Statistical Learning");
        User f4 = createFacultyUser("Dr. Robert Wilson", "robert.wilson@research.com", "Robert@123", "Internet of Things", "IoT, Sensor Networks", "Smart Cities, Edge Computing");
        User f5 = createFacultyUser("Dr. Kavya Nair", "kavya.nair@research.com", "Kavya@123", "Natural Language Processing", "NLP, Transformers", "Large Language Models, Text Mining");
        User f6 = createFacultyUser("Dr. David Kim", "david.kim@research.com", "David@123", "Blockchain", "Smart Contracts, Distributed Ledgers", "Cryptocurrency, Consensus Algorithms");
        User f7 = createFacultyUser("Dr. Elena Rossi", "elena.rossi@research.com", "Elena@123", "Robotics", "Autonomous Systems, Kinematics", "Reinforcement Learning, Path Planning");

        // 2. Seed Students
        User s1 = createStudentUser("Arjun Kumar", "arjun.kumar@research.com", "Arjun@123");
        User s2 = createStudentUser("Ananya Sharma", "ananya.sharma@research.com", "Ananya@123");
        User s3 = createStudentUser("Rahul Verma", "rahul.verma@research.com", "Rahul@123");
        User s4 = createStudentUser("Sneha Iyer", "sneha.iyer@research.com", "Sneha@123");
        User s5 = createStudentUser("Vikram Singh", "vikram.singh@research.com", "Vikram@123");
        User s6 = createStudentUser("Meera Krishnan", "meera.krishnan@research.com", "Meera@123");
        User s7 = createStudentUser("Rohan Patel", "rohan.patel@research.com", "Rohan@123");
        User s8 = createStudentUser("Divya Menon", "divya.menon@research.com", "Divya@123");
        User s9 = createStudentUser("Aditya Rao", "aditya.rao@research.com", "Aditya@123");
        User s10 = createStudentUser("Ishita Gupta", "ishita.gupta@research.com", "Ishita@123");
        User s11 = createStudentUser("Karthik Reddy", "karthik.reddy@research.com", "Karthik@123");
        User s12 = createStudentUser("Nisha Kapoor", "nisha.kapoor@research.com", "Nisha@123");
        User s13 = createStudentUser("Aarav Joshi", "aarav.joshi@research.com", "Aarav@123");
        User s14 = createStudentUser("Pooja Nair", "pooja.nair@research.com", "Pooja@123");

        // 3. Seed Projects
        Project p1 = createProject("AI-Powered Healthcare Diagnosis System", 
                "An intelligent system leveraging CNNs for medical imaging.", 
                "Artificial Intelligence", "deep learning, classification, CNN, diagnosis", s1.getUserId());
        Project p2 = createProject("Intelligent Network Intrusion Detection Platform", 
                "A platform detecting network anomalies using machine learning.", 
                "Cybersecurity", "intrusion detection, network security, anomaly detection, cybersecurity", s2.getUserId());
        Project p3 = createProject("Smart City IoT Monitoring System", 
                "Monitoring smart city infrastructure via IoT edge nodes.", 
                "Internet of Things", "IoT, sensors, smart city, edge computing, real-time monitoring", s3.getUserId());
        Project p4 = createProject("Transformer-Based Academic Research Assistant", 
                "An LLM-powered tool to parse academic papers.", 
                "Natural Language Processing", "NLP, transformers, LLM, text mining, semantic search", s4.getUserId());
        Project p5 = createProject("Blockchain-Based Academic Certificate Verification", 
                "Verifying certificates securely on the blockchain.", 
                "Blockchain", "blockchain, smart contracts, digital certificates, authentication", s5.getUserId());
        Project p6 = createProject("Predictive Student Performance Analytics", 
                "Using data mining to predict student dropouts and performance.", 
                "Data Science", "predictive analytics, data mining, classification, student analytics", s6.getUserId());
        Project p7 = createProject("Autonomous Robot Navigation System", 
                "A vision-based autonomous navigation pipeline.", 
                "Robotics", "robotics, computer vision, path planning, object detection", s7.getUserId());
        Project p8 = createProject("Cloud-Based Collaborative Research Repository", 
                "Scalable collaborative research repository.", 
                "Cloud Computing", "cloud computing, distributed systems, scalable storage, collaboration", s8.getUserId());
        Project p9 = createProject("Advanced Threat Intelligence Platform", 
                "Aggregating threats using zero trust architecture.", 
                "Cybersecurity", "threat intelligence, zero trust, network security", s9.getUserId());
        Project p10 = createProject("Edge Computing for Smart Vehicles", 
                "Low latency edge analytics for autonomous vehicles.", 
                "Internet of Things", "edge computing, IoT, smart vehicles, sensors", s10.getUserId());


        // 4. Seed Publications for Faculty
        seedPublication("Advances in Explainable Deep Learning", "Journal of Artificial Intelligence", 2024, "Artificial Intelligence", "deep learning, explainable AI", f1);
        seedPublication("Vision-Based Traffic Intelligence", "IEEE Transactions on ITS", 2023, "Artificial Intelligence", "computer vision, traffic", f1);
        seedPublication("Deep Neural Networks for Medical Imaging", "Healthcare AI", 2025, "Artificial Intelligence", "CNN, medical imaging", f1);
        seedPublication("Secure Network Intrusion Detection Using Machine Learning", "Cybersecurity Reviews", 2024, "Cybersecurity", "network security, intrusion detection", f2);
        seedPublication("Zero Trust Architecture for Distributed Systems", "Security Journal", 2023, "Cybersecurity", "zero trust, distributed systems", f2);
        seedPublication("Threat Intelligence in the Modern Era", "InfoSec Today", 2026, "Cybersecurity", "threat intelligence", f2);
        seedPublication("Predictive Analytics for Smart Cities", "Data Science Monthly", 2022, "Data Science", "predictive analytics, smart cities", f3);
        seedPublication("Scalable Data Mining for Large Datasets", "Big Data Analytics", 2025, "Data Science", "data mining, big data", f3);
        seedPublication("Edge Computing for Intelligent IoT", "IoT Journal", 2024, "Internet of Things", "edge computing, IoT", f4);
        seedPublication("Secure Sensor Networks for Smart Infrastructure", "Sensor Networks", 2023, "Internet of Things", "sensor networks, smart infrastructure", f4);
        seedPublication("Transformer Models for Domain-Specific NLP", "NLP Research", 2025, "Natural Language Processing", "transformers, NLP, LLM", f5);
        seedPublication("Efficient Text Classification Using Deep Learning", "Computational Linguistics", 2022, "Natural Language Processing", "text mining, classification", f5);
        seedPublication("Smart Contracts for Supply Chain", "Blockchain Tech", 2024, "Blockchain", "blockchain, smart contracts", f6);
        seedPublication("Decentralized Consensus Mechanisms", "Crypto Journal", 2026, "Blockchain", "cryptocurrency, consensus", f6);
        seedPublication("Kinematics of Autonomous Robots", "Robotics Today", 2021, "Robotics", "robotics, kinematics", f7);
        seedPublication("Reinforcement Learning in Path Planning", "AI & Robotics", 2025, "Robotics", "path planning, reinforcement learning", f7);

        // Faculty Alan Turing (if exists)
        User alan = userRepository.findByEmail("alan@research.com").orElse(null);
        if (alan != null) {
            seedPublication("Foundations of Computing", "Computer Journal", 2021, "Computer Science", "computing, theory", alan);
            seedPublication("Turing Machines in Modern AI", "AI History", 2022, "Artificial Intelligence", "theory, AI", alan);
        }

        // Faculty Ada Lovelace (if exists)
        User ada = userRepository.findByEmail("ada@research.com").orElse(null);
        if (ada != null) {
            seedPublication("Early Programming Concepts", "History of Algorithms", 2021, "Software Engineering", "programming", ada);
            seedPublication("Analytical Engine Implications", "Tech History", 2024, "Computer Science", "hardware, algorithms", ada);
        }

        // 5. Seed Collaborations
        seedCollaboration(p1.getProjectId(), f1, s1.getUserId(), "PENDING");
        seedCollaboration(p2.getProjectId(), f2, s2.getUserId(), "ACCEPTED");
        seedCollaboration(p3.getProjectId(), f4, s3.getUserId(), "PENDING");
        seedCollaboration(p4.getProjectId(), f5, s4.getUserId(), "ACCEPTED");
        seedCollaboration(p5.getProjectId(), f6, s5.getUserId(), "REJECTED");
        seedCollaboration(p6.getProjectId(), f3, s6.getUserId(), "ACCEPTED");
        seedCollaboration(p7.getProjectId(), f7, s7.getUserId(), "REJECTED");
        seedCollaboration(p8.getProjectId(), f4, s8.getUserId(), "PENDING");
        seedCollaboration(p9.getProjectId(), f2, s9.getUserId(), "ACCEPTED");
        seedCollaboration(p10.getProjectId(), f4, s10.getUserId(), "PENDING");

        System.out.println("Demo data seeding completed.");
    }

    private User createFacultyUser(String name, String email, String pwd, String dept, String exp, String interests) {
        return userRepository.findByEmail(email).orElseGet(() -> {
            User u = new User();
            u.setName(name);
            u.setEmail(email);
            u.setPassword(passwordEncoder.encode(pwd));
            u.setRole("FACULTY");
            userRepository.save(u);
            
            Faculty f = new Faculty();
            f.setUserId(u.getUserId());
            f.setDepartment(dept);
            f.setExpertise(exp);
            f.setResearchInterests(interests);
            f.setAvailability("Available");
            facultyRepository.save(f);
            
            return u;
        });
    }

    private User createStudentUser(String name, String email, String pwd) {
        return userRepository.findByEmail(email).orElseGet(() -> {
            User u = new User();
            u.setName(name);
            u.setEmail(email);
            u.setPassword(passwordEncoder.encode(pwd));
            u.setRole("STUDENT");
            return userRepository.save(u);
        });
    }

    private Project createProject(String title, String desc, String domain, String keywords, Integer studentId) {
        return projectRepository.findAll().stream().filter(p -> p.getTitle().equals(title)).findFirst().orElseGet(() -> {
            Project p = new Project();
            p.setTitle(title);
            p.setDescription(desc);
            p.setDomain(domain);
            p.setKeywords(keywords);
            p.setStudentId(studentId);
            p.setStatus("OPEN");
            return projectRepository.save(p);
        });
    }

    private void seedPublication(String title, String journal, int year, String domain, String keywords, User facultyUser) {
        Optional<Faculty> facOpt = facultyRepository.findByUserId(facultyUser.getUserId());
        if (facOpt.isEmpty()) return;
        
        Integer facId = facOpt.get().getFacultyId();
        boolean exists = publicationRepository.findAll().stream().anyMatch(p -> p.getTitle().equals(title));
        
        if (!exists) {
            Publication pub = new Publication();
            pub.setTitle(title);
            pub.setJournal(journal);
            pub.setYear(year);
            pub.setDomain(domain);
            pub.setKeywords(keywords);
            pub.setFacultyId(facId);
            publicationRepository.save(pub);
        }
    }

    private void seedCollaboration(Integer projectId, User facultyUser, Integer studentId, String status) {
        Optional<Faculty> facOpt = facultyRepository.findByUserId(facultyUser.getUserId());
        if (facOpt.isEmpty()) return;
        
        Integer facId = facOpt.get().getFacultyId();
        boolean exists = collaborationRepository.findAll().stream()
                .anyMatch(c -> c.getProjectId().equals(projectId) && c.getFacultyId().equals(facId) && c.getStudentId().equals(studentId));
        
        if (!exists) {
            Collaboration col = new Collaboration();
            col.setProjectId(projectId);
            col.setFacultyId(facId);
            col.setStudentId(studentId);
            col.setStatus(status);
            collaborationRepository.save(col);
        }
    }
}
