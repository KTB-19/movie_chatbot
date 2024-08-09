package com.ktb19.moviechatbot.dto;

import com.ktb19.moviechatbot.entity.MovieInfo;
import com.ktb19.moviechatbot.entity.Movie;
import com.ktb19.moviechatbot.entity.Theater;
import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.Setter;

@Getter
@Setter
@AllArgsConstructor
public class MovieInfoDetailsQueryDto {

    private MovieInfo movieInfo;
    private Movie movie;
    private Theater theater;

}
