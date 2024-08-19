package com.ktb19.moviechatbot.dto;

import com.fasterxml.jackson.annotation.JsonFormat;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.Pattern;
import jakarta.validation.constraints.Size;
import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

import java.time.LocalDate;
import java.time.LocalTime;

@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
public class MovieRunningTimesRequest {

    @NotBlank
    @Pattern(regexp = "^[가-힣a-zA-Z0-9!#$%&'*+/=?`{|}~^.-]*$", message = "한글, 영어, 숫자, 특수문자만 입력할 수 있습니다.")
    @Size(min = 1, max = 100)
    private String movieName;

    @NotBlank
    @Pattern(regexp = "^[가-힣 ]*$", message = "한글, 띄어쓰기만 입력할 수 있습니다.")
    @Size(min = 1, max = 30)
    private String region;

    @JsonFormat(shape = JsonFormat.Shape.STRING, pattern = "yyyy-MM-dd", timezone = "Asia/Seoul")
    @NotNull
    private LocalDate date;

    @JsonFormat(shape = JsonFormat.Shape.STRING, pattern = "HH:MM", timezone = "Asia/Seoul")
    private LocalTime time;

}
