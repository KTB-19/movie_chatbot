package com.ktb19.moviechatbot.controller;

import com.ktb19.moviechatbot.dto.*;
import com.ktb19.moviechatbot.entity.Movie;
import com.ktb19.moviechatbot.service.MovieService;
import com.ktb19.moviechatbot.service.ParseService;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.Parameter;
import io.swagger.v3.oas.annotations.media.ArraySchema;
import io.swagger.v3.oas.annotations.media.Content;
import io.swagger.v3.oas.annotations.media.Schema;
import io.swagger.v3.oas.annotations.responses.ApiResponse;
import io.swagger.v3.oas.annotations.responses.ApiResponses;
import io.swagger.v3.oas.annotations.tags.Tag;
import jakarta.validation.Valid;
import jakarta.validation.constraints.Pattern;
import jakarta.validation.constraints.Size;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

/**
 * 영화 관련 쿼리와 상영 시간 정보를 처리하는 API를 제공합니다.
 */
@Slf4j
@Tag(name = "Movie", description = "Movie API")
@RestController
@RequiredArgsConstructor
@RequestMapping("/api/v1")
public class MovieController {

    private final ParseService parseService;
    private final MovieService movieService;

    /**
     * 메시지를 파싱하여 영화 이름, 지역, 날짜, 시간을 추출합니다.
     *
     * @param message 영화 제목, 지역, 날짜, 시간 중 일부를 담은 사용자 메시지
     * @return 파싱된 결과를 포함한 ResponseEntity 객체
     */
    @Operation(summary = "메시지 파싱", description = "메시지를 파싱하여 영화 이름, 지역, 날짜, 시간을 추출", operationId = "1")
    @ApiResponse(responseCode = "200", description = "성공적으로 파싱된 결과 반환",
            content = @Content(schema = @Schema(implementation = ParsedQueryResponse.class)))
    @GetMapping("/movie/query")
    public ResponseEntity<?> getParsedQuery(
            @Parameter(
                    description = "영화 제목, 지역, 날짜, 시간 중 일부를 담은 사용자 메시지",
                    required = true,
                    example = "에일리언 오늘 오후 5시에 보고 싶어"
            )
            @RequestParam
            @Size(min = 1, max = 200)
            @Pattern(
                    regexp = "^[가-힣ㄱ-ㅎㅏ-ㅣa-zA-Z0-9 !#$%&'*+/=?`{|}~^.-:]*$",
                    message = "한글, 영어, 숫자, 특수문자만 입력할 수 있습니다."
            )
            String message) {

        return ResponseEntity.ok(ParsedQueryResponse.of(parseService.parse(message)));
    }

    /**
     * 이전에 파싱된 결과와 부족한 정보에 대한 사용자의 메시지를 같이 받아, 완성된 영화 이름, 지역, 날짜, 시간이 포함된 객체를 반환합니다.
     *
     * @param request 이전에 파싱된 결과와 부족한 정보에 대한 사용자의 추가 메세지를 담고 있는 AdditionalQueryRequest 객체
     * @return 파싱된 쿼리 결과를 포함한 ResponseEntity 객체
     */
    @Operation(summary = "추가 메세지 파싱",
            description = "이전에 파싱된 결과와 부족한 정보에 대한 사용자의 메시지를 같이 받아, 완성된 영화 이름, 지역, 날짜, 시간이 포함된 객체를 반환",
            operationId = "2")
    @ApiResponse(responseCode = "200", description = "성공적으로 추가 파싱된 결과 반환",
            content = @Content(schema = @Schema(implementation = AdditionalParsedQueryResponse.class)))
    @PostMapping("/movie/query/additional")
    public ResponseEntity<?> getParsedQueryByAdditionalQuery(
            @Parameter(
                    description = "이전에 파싱된 결과와 부족한 정보에 대한 사용자의 추가 메세지를 담고 있는 AdditionalQueryRequest 객체",
                    required = true
            )
            @RequestBody @Valid AdditionalQueryRequest request) {
        return ResponseEntity.ok(AdditionalParsedQueryResponse.of(parseService.parseAdditional(request)));
    }

    /**
     * 영화의 상영 시간을 조회합니다.
     *
     * @param parsedQuery 파싱된 정보를 담고 있는 MovieRunningTimesRequest 객체
     * @return 상영 시간 정보를 포함한 ResponseEntity 객체
     */
    @Operation(summary = "영화 상영 시간 조회",
            description = """
                    파싱된 영화 정보를 기반으로 상영 시간 조회 \n
                    time이 null일 경우, 당일 모든 상영 정보 조회 \n
                    time이 null이 아닐 경우, 해당 시간 이후의 모든 상영 정보 조회
                    """,
            operationId = "3")
    @ApiResponse(responseCode = "200", description = "성공적으로 영화 상영 시간 조회 결과 반환",
            content = @Content(schema = @Schema(implementation = MovieRunningTimesDto.class)))
    @PostMapping("/movie/running-times")
    public ResponseEntity<?> getRunningTimes(
            @Parameter(
                    description = "파싱된 정보를 담고 있는 MovieRunningTimesRequest 객체",
                    required = true
            )
            @RequestBody @Valid MovieRunningTimesRequest parsedQuery) {
        return ResponseEntity.ok(movieService.getRunningTimes(parsedQuery));
    }
}
