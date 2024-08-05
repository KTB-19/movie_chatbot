package com.ktb19.moviechatbot.dto;

import com.ktb19.moviechatbot.entity.Info;
import com.ktb19.moviechatbot.entity.Movie;
import com.ktb19.moviechatbot.entity.Theater;
import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.Setter;

@Getter
@Setter
@AllArgsConstructor
public class InfoDetailsQueryDto {

    private Info info;
    private Movie movie;
    private Theater theater;

}
