package com.ktb19.moviechatbot.repository;

import com.ktb19.moviechatbot.entity.Info;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface InfoRepository extends JpaRepository<Info, Long> {
}
