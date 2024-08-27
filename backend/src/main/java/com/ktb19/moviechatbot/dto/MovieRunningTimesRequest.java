package com.ktb19.moviechatbot.dto;

import com.fasterxml.jackson.annotation.JsonFormat;
import io.swagger.v3.oas.annotations.media.Schema;
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

@Schema(description = "상영 정보 요청")
@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
public class MovieRunningTimesRequest {

    @Schema(description = "영화 이름", example = "에이리언 : 로물루스")
    @NotBlank
    @Pattern(regexp = "^[가-힣ㄱ-ㅎㅏ-ㅣa-zA-Z0-9 !#$%&'*+/=?`{|}~^.-:]*$", message = "한글, 영어, 숫자, 특수문자만 입력할 수 있습니다.")
    @Size(min = 1, max = 100)
    private String movieName;

    @Schema(description = "지역", example = "대구 동성로")
    @NotBlank
    @Pattern(regexp = "^[가-힣 ]*$", message = "한글, 띄어쓰기만 입력할 수 있습니다.")
    @Size(min = 1, max = 30)
    private String region;

    @Schema(description = "상영 날짜", example = "2024-08-14")
    @JsonFormat(shape = JsonFormat.Shape.STRING, pattern = "yyyy-MM-dd", timezone = "Asia/Seoul")
    @NotNull
    private LocalDate date;

    @Schema(description = "상영 시간", example = "17:00", type = "string")
    @JsonFormat(shape = JsonFormat.Shape.STRING, pattern = "HH:mm", timezone = "Asia/Seoul")
    private LocalTime time;

}
