package com.ktb19.moviechatbot.dto;

import lombok.Getter;
import lombok.Setter;

import java.util.Date;

@Getter
@Setter
public class QueryDto {

    private String movieName;
    private String region;
    private Date date;
}
