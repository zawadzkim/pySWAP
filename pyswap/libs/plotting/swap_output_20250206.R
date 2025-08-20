#-------------------------------------------------------------------------
# SWAP-output.rds
# H.M. Mulder
# Wageningen Environmental research
#-------------------------------------------------------------------------

setwd("c:/Users/mulde027/Software/R/Variables/SWAP_variables")

# load R-packages
library(readr)

lstvar <- list()

# ---- SWAP (time-depth) ----

# FLUX
var <- list()
var$type <- "time-depth"
var$variable <- "FLUX[depth]"
var$variable_type <- "rate"
var$colour <- "blue"
var$graph_type <- "line"
var$labels_EN <- "[depth] cm"
var$labels_NL <- "[depth] cm"
var$y_label_EN <- "bottomflux"
var$y_label_NL <- "flux onderrand"
var$unit <- "mm d-1"
var$factor <- 10
lstvar$FLUX <- var

# WC
var <- list()
var$type <- "time-depth"
var$variable <- "WC[depth]"
var$variable_type <- "state"
var$colour <- "blue"
var$colours <- "viridis"
var$flip_colours <- TRUE
var$graph_type <- "line"
var$labels_EN <- "[depth] cm"
var$labels_NL <- "[depth] cm"
var$y_label_EN <- "water content"
var$y_label_NL <- "watergehalte"
var$unit <- "cm3 cm-3"
lstvar$WC <- var

# H
var <- list()
var$type <- "time-depth"
var$variable <- "H[depth]"
var$variable_type <- "state"
var$colour <- "blue"
var$colours <- "viridis"
var$flip_colours <- TRUE
var$graph_type <- "line"
var$labels_EN <- "[depth] cm"
var$labels_NL <- "[depth] cm"
var$y_label_EN <- "pressure head"
var$y_label_NL <- "drukhoogte"
var$unit <- "cm"
lstvar$H <- var

# H_LOG
var <- list()
var$type <- "time-depth"
var$variable <- "H[depth]"
var$variable_type <- "state"
var$colour <- "blue"
var$colours <- "viridis"
var$flip_colours <- TRUE
var$graph_type <- "line"
var$labels_EN <- "[depth] cm"
var$labels_NL <- "[depth] cm"
var$y_label_EN <- "pressure head"
var$y_label_NL <- "drukhoogte"
var$unit <- "pF"
var$expression <- "log10(pmax(-H, 1.0))"
lstvar$H_LOG <- var

# K
var <- list()
var$type <- "time-depth"
var$variable <- "K[depth]"
var$variable_type <- "state"
var$colour <- "darkgoldenrod2"
var$colours <- "viridis"
var$flip_colours <- TRUE
var$graph_type <- "line"
var$labels_EN <- "[depth] cm"
var$labels_NL <- "[depth] cm"
var$y_label_EN <- "hydraulic conductivity"
var$y_label_NL <- "doorlatendheid"
var$factor <- 0.1
var$unit <- "mm"
lstvar$K <- var

# TEMP
var <- list()
var$type <- "time-depth"
var$variable <- "TEMP[depth]"
var$variable_type <- "state"
var$colour <- "darkred"
var$colours <- "coolwarm"
var$flip_colours <- FALSE
var$graph_type <- "line"
var$labels_EN <- "[depth] cm"
var$labels_NL <- "[depth] cm"
var$y_label_EN <- "temperature"
var$y_label_NL <- "temperatuur"
var$unit <- "oC"
lstvar$TEMP <- var

# HEACAP
var <- list()
var$type <- "time-depth"
var$variable <- "HEACAP[depth]"
var$variable_type <- "state"
var$colour <- "darkred"
var$colours <- "coolwarm"
var$flip_colours <- FALSE
var$graph_type <- "line"
var$labels_EN <- "[depth] cm"
var$labels_NL <- "[depth] cm"
var$y_label_EN <- "soil heat capacity"
var$y_label_NL <- "warmte capaciteit bodem"
var$unit <- "J m-3 K-1"
lstvar$HEACAP <- var

# HEACON
var <- list()
var$type <- "time-depth"
var$variable <- "HEACON[depth]"
var$variable_type <- "state"
var$colour <- "darkred"
var$colours <- "coolwarm"
var$flip_colours <- FALSE
var$graph_type <- "line"
var$labels_EN <- "[depth] cm"
var$labels_NL <- "[depth] cm"
var$y_label_EN <- "soil heat conductivity"
var$y_label_NL <- "warmtegeleiding bodem"
var$unit <- "W m-1 K-1"
lstvar$HEACON <- var

# CONC
var <- list()
var$type <- "time-depth"
var$variable <- "CONC[depth]"
var$variable_type <- "state"
var$colour <- "orange"
var$colours <- "viridis"
var$flip_colours <- FALSE
var$graph_type <- "line"
var$labels_EN <- "[depth] cm"
var$labels_NL <- "[depth] cm"
var$y_label_EN <- "salinity concentration"
var$y_label_NL <- "zoutconcentratie"
var$unit <- "mg l-1"
lstvar$CONC <- var

# CONCADS
var <- list()
var$type <- "time-depth"
var$variable <- "CONCADS[depth]"
var$variable_type <- "state"
var$colour <- "orange"
var$colours <- "viridis"
var$flip_colours <- TRUE
var$graph_type <- "line"
var$labels_EN <- "[depth] cm"
var$labels_NL <- "[depth] cm"
var$y_label_EN <- "absorbed solute"
var$y_label_NL <- "opgelost zout"
var$unit <- "mg l-1"
lstvar$CONCADS <- var

# O2TOP
var <- list()
var$type <- "time-depth"
var$variable <- "O2TOP[depth]"
var$variable_type <- "state"
var$colour <- "blue"
var$colours <- "coolwarm"
var$flip_colours <- TRUE
var$graph_type <- "line"
var$labels_EN <- "[depth] cm"
var$labels_NL <- "[depth] cm"
var$y_label_EN <- "oxygen concentration"
var$y_label_NL <- "concentratie zuurstof"
var$unit <- "kg m-3"
lstvar$O2TOP <- var

# STRESS
var <- list()
var$type <- "time-depth"
var$variable <- c("PRWU", "RRWU", "RDENS")
var$variable_type <- "state"
var$colour <- "blue"
var$colours <- "viridis"
var$flip_colours <- FALSE
var$labels_EN <- "[depth] cm"
var$labels_NL <- "[depth] cm"
var$y_label_EN <- "stress"
var$y_label_NL <- "stress"
var$unit <- "%"
lstvar$STRESS <- var

# PRWU
var <- list()
var$type <- "time-depth"
var$variable <- "PRWU"
var$variable_type <- "rate"
var$colour <- "blue"
var$colours <- "viridis"
var$flip_colours <- FALSE
var$labels_EN <- "[depth] cm"
var$labels_NL <- "[depth] cm"
var$y_label_EN <- "pot. root water uptake"
var$y_label_NL <- "pot. wateropname"
var$unit <- "mm d-1"
lstvar$PRWU <- var

# RWU
var <- list()
var$type <- "time-depth"
var$variable <- "RWU"
var$variable_type <- "rate"
var$colour <- "blue"
var$colours <- "viridis"
var$flip_colours <- FALSE
var$labels_EN <- "[depth] cm"
var$labels_NL <- "[depth] cm"
var$y_label_EN <- "root water uptake"
var$y_label_NL <- "wateropname"
var$unit <- "mm d-1"
lstvar$RWU <- var

# RDENS
var <- list()
var$type <- "time-depth"
var$variable <- "RDENS"
var$variable_type <- "state"
var$colour <- "green"
var$colours <- "viridis"
var$flip_colours <- FALSE
var$labels_EN <- "[depth] cm"
var$labels_NL <- "[depth] cm"
var$y_label_EN <- "rel. root density"
var$y_label_NL <- "rel. worteldichtheid"
var$unit <- "-"
lstvar$RDENS <- var

# LRV
var <- list()
var$type <- "time-depth"
var$variable <- "LRV[depth]"
var$variable_type <- "state"
var$colour <- "green"
var$colours <- "viridis"
var$flip_colours <- FALSE
var$graph_type <- "line"
var$labels_EN <- "[depth] cm"
var$labels_NL <- "[depth] cm"
var$y_label_EN <- "Lrv"
var$y_label_NL <- "Lrv"
var$unit <- "cm cm-3"
lstvar$LRV <- var

# ---- SWAP (time-range) ----

# QTOP
var <- list()
var$type <- "time-range"
var$variable <- "QTOP[depth]"
var$variable_type <- "rate"
var$colour <- "blue"
var$graph_type <- "bar"
var$labels_EN <- "[depth] cm"
var$labels_NL <- "[depth] cm"
var$y_label_EN <- "top boundary"
var$y_label_NL <- "bovenrand"
var$unit <- "mm"
var$factor <- 10
lstvar$QTOP <- var

# QTOPIN
var <- list()
var$type <- "time-range"
var$variable <- "QTOPIN[depth]"
var$variable_type <- "rate"
var$colour <- "blue"
var$graph_type <- "bar"
var$labels_EN <- "[depth] cm"
var$labels_NL <- "[depth] cm"
var$y_label_EN <- "top boundary in"
var$y_label_NL <- "bovenrand in"
var$unit <- "mm"
var$factor <- 10
lstvar$QTOPIN <- var

# QTOPOUT
var <- list()
var$type <- "time-range"
var$variable <- "QTOPOUT[depth]"
var$variable_type <- "rate"
var$colour <- "blue"
var$graph_type <- "bar"
var$labels_EN <- "[depth] cm"
var$labels_NL <- "[depth] cm"
var$y_label_EN <- "top boundary out"
var$y_label_NL <- "bovenrand uit"
var$unit <- "mm"
var$factor <- 10
lstvar$QTOPOUT <- var

# QBOT
var <- list()
var$type <- "time-range"
var$variable <- "QBOT[depth]"
var$variable_type <- "rate"
var$colour <- "blue"
var$graph_type <- "bar"
var$labels_EN <- "[depth] cm"
var$labels_NL <- "[depth] cm"
var$y_label_EN <- "bottom boundary"
var$y_label_NL <- "onderrand"
var$unit <- "mm"
var$factor <- 10
lstvar$QBOT <- var

# QBOTIN
var <- list()
var$type <- "time-range"
var$variable <- "QBOTIN[depth]"
var$variable_type <- "rate"
var$colour <- "blue"
var$graph_type <- "bar"
var$labels_EN <- "[depth] cm"
var$labels_NL <- "[depth] cm"
var$y_label_EN <- "bottom boundary in"
var$y_label_NL <- "onderrand in"
var$unit <- "mm"
var$factor <- 10
lstvar$QBOTIN <- var

# QBOTOUT
var <- list()
var$type <- "time-range"
var$variable <- "QBOTOUT[depth]"
var$variable_type <- "rate"
var$colour <- "blue"
var$graph_type <- "bar"
var$labels_EN <- "[depth] cm"
var$labels_NL <- "[depth] cm"
var$y_label_EN <- "bottom boundary out"
var$y_label_NL <- "onderrand uit"
var$unit <- "mm"
var$factor <- 10
lstvar$QBOTOUT <- var

# QDRA
var <- list()
var$type <- "time-range"
var$variable <- "QDRA[depth]"
var$variable_type <- "rate"
var$colour <- "blue"
var$graph_type <- "bar"
var$labels_EN <- "[depth] cm"
var$labels_NL <- "[depth] cm"
var$y_label_EN <- "drainage"
var$y_label_NL <- "drainage"
var$unit <- "mm"
var$factor <- 10
lstvar$QDRA <- var

# QDRAININ
var <- list()
var$type <- "time-range"
var$variable <- "QDRAININ[depth]"
var$variable_type <- "rate"
var$colour <- "blue"
var$graph_type <- "bar"
var$labels_EN <- "[depth] cm"
var$labels_NL <- "[depth] cm"
var$y_label_EN <- "drainage in"
var$y_label_NL <- "drainage in"
var$unit <- "mm"
var$factor <- 10
lstvar$QDRAININ <- var

# QDRAINOUT
var <- list()
var$type <- "time-range"
var$variable <- "QDRAINOUT[depth]"
var$variable_type <- "rate"
var$colour <- "blue"
var$graph_type <- "bar"
var$labels_EN <- "[depth] cm"
var$labels_NL <- "[depth] cm"
var$y_label_EN <- "drainage out"
var$y_label_NL <- "drainage uit"
var$unit <- "mm"
var$factor <- 10
lstvar$QDRAINOUT <- var

# QTRANS
var <- list()
var$type <- "time-range"
var$variable <- "QTRANS[depth]"
var$variable_type <- "rate"
var$colour <- "blue"
var$graph_type <- "bar"
var$labels_EN <- "[depth] cm"
var$labels_NL <- "[depth] cm"
var$y_label_EN <- "transpiration"
var$y_label_NL <- "transpiratie"
var$unit <- "mm"
var$factor <- 10
lstvar$QTRANS <- var

# WTOT
var <- list()
var$type <- "time-range"
var$variable <- "WTOT[depth]"
var$variable_type <- "state"
var$colour <- "blue"
var$graph_type <- "bar"
var$labels_EN <- "[depth] cm"
var$labels_NL <- "[depth] cm"
var$y_label_EN <- "storage"
var$y_label_NL <- "berging"
var$unit <- "mm"
var$factor <- 10
lstvar$WTOT <- var

# SUBREG_MIN
var <- list()
var$type <- "time-range"
var$variable <- c("QTOP[depth]", "QTRANS[depth]", "QDRA[depth]", "WTOT[depth]", "QBOT[depth]")
var$variable_optional <- c("QTRANS[depth]", "QDRA[depth]", "QBOT[depth]")
var$variable_type <- "rate"
var$levels <- c("QTOP", "QTRANS", "QDRA", "DSTOR", "QBOT")
var$colours <- c("dodgerblue3", "darkgreen", "goldenrod4", "cornsilk3", "darkblue")
var$graph_type <- "bar"
var$labels_EN <- c("top", "transpiration", "drainage", "storage", "bottom")
var$labels_NL <- c("boven", "transpiratie", "drainage", "berging", "onder")
var$y_label_EN <- "net water balance"
var$y_label_NL <- "netto waterbalans"
var$unit <- "mm"
var$factor <- 10
lstvar$SUBREG_MIN <- var

# SUBREG_ALL
var <- list()
var$type <- "time-range"
var$variable <- c("QTOPIN[depth]", "QTOPOUT[depth]", "QTRANS[depth]", "QDRAININ[depth]", "QDRAINOUT[depth]", "WTOT[depth]", "QBOTIN[depth]", "QBOTOUT[depth]")
var$variable_optional <- c("QTRANS[depth]", "QDRAININ[depth]", "QDRAINOUT[depth]", "QBOTIN[depth]", "QBOTOUT[depth]")
var$variable_type <- "rate"
var$levels <- c("QTOPIN", "QTOPOUT", "QTRANS", "QDRAININ", "QDRAINOUT", "DSTOR", "QBOTIN", "QBOTOUT")
var$colours <- c("dodgerblue3", "dodgerblue3", "darkgreen", "goldenrod4", "goldenrod4", "cornsilk3", "darkblue", "darkblue")
var$graph_type <- "bar"
var$labels_EN <- c("top", "top", "transpiration", "drainage", "drainage", "storage", "bottom", "bottom")
var$labels_NL <- c("boven", "boven", "transpiratie", "drainage", "drainage", "berging", "onder", "onder")
var$y_label_EN <- "water balance"
var$y_label_NL <- "waterbalans"
var$unit <- "mm"
var$factor <- 10
lstvar$SUBREG_ALL <- var

# ---- SWAP (time) ----

# WATBAL_PLOT
var <- list()
var$type <- "time"
var$variable <- c("RAIN", "SNOW", "IRRIG", "RUNON", "RUNOFF", "INTERC", "TACT", "EACT", "SUBLIM", "QSSDI", "DRAINAGE", "DSTOR", "QBOTTOM")
var$variable_optional <- c("SNOW", "INTERC", "RUNON", "TACT", "SUBLIM", "QSSDI", "DRAINAGE", "QBOTTOM")
var$variable_type <- "rate"
var$levels <- c("RAIN", "SNOW", "IRRIG", "RUNON", "RUNOFF", "INTERC", "TACT", "EACT", "SUBLIM", "QSSDI", "DRAINAGE", "DSTOR", "QBOTTOM")
var$colours <- c("dodgerblue3", "wheat", "lightblue", "red", "darkred", "darkolivegreen1", "darkgreen", "darkorange", "wheat4", "sienna", "goldenrod4", "cornsilk3", "darkblue")
var$graph_type <- "bar"
var$labels_EN <- c("precipitation", "snow", "irrigation", "runon", "runoff", "interception", "transpiration", "evaporation", "snow sublimated", "subirrigation", "drainage", "storage", "bottomflux")
var$labels_NL <- c("neerslag", "sneeuw", "irrigatie", "aanstroming", "afstroming", "interceptie", "transpiratie", "evaporatie", "gesublimeerd sneeuw", "subirrigatie", "drainage", "berging", "onderrand")
var$y_label_EN <- "net water balance"
var$y_label_NL <- "netto waterbalans"
var$unit <- "mm"
var$factor <- 10
lstvar$WATBAL_PLOT <- var

# DRAINAGE_PLOT
var <- list()
var$type <- "time"
var$variable <- c("DRAINAGE_1", "DRAINAGE_2", "DRAINAGE_3", "DRAINAGE_4", "DRAINAGE_5")
var$variable_optional <- c("DRAINAGE_1", "DRAINAGE_2", "DRAINAGE_3", "DRAINAGE_4", "DRAINAGE_5")
var$variable_type <- "rate"
var$levels <- c("DRAINAGE_1", "DRAINAGE_2", "DRAINAGE_3", "DRAINAGE_4", "DRAINAGE_5")
var$colours <- c("goldenrod4", "goldenrod3", "gold2", "lightgoldenrod2", "wheat")
var$graph_type <- "bar"
var$labels_EN <- c("system 1", "system 2", "system 3", "system 4", "system 5")
var$labels_NL <- c("systeem 1", "systeem 2", "systeem 3", "systeem 4", "systeem 5")
var$y_label_EN <- "net drainage"
var$y_label_NL <- "netto drainage"
var$unit <- "mm"
var$factor <- 10
lstvar$DRAINAGE_PLOT <- var

# ETACT_PLOT
var <- list()
var$type <- "time"
var$variable <- c("INTERC", "TACT", "EACT")
var$variable_optional <- c("INTERC", "TACT")
var$variable_type <- "rate"
var$levels <- c("INTERC", "TACT", "EACT")
var$colours <- c("lightblue", "darkgreen", "orange")
var$graph_type <- "bar"
var$labels_EN <- c("interception", "transpiration", "evaporation")
var$labels_NL <- c("interceptie", "transpiratie", "evaporatie")
var$y_label_EN <- "evapotranspiration"
var$y_label_NL <- "evapotranspiratie"
var$unit <- "mm"
var$factor <- 10
lstvar$ETACT_PLOT <- var

# TRED_PLOT
var <- list()
var$type <- "time"
var$variable <- c("TPOT", "TREDDRY", "TREDWET", "TREDSOL", "TREDFRS")
var$variable_optional <- c("TREDWET", "TREDSOL", "TREDFRS")
var$variable_type <- "rate"
var$levels <- c("TREDDRY", "TREDWET", "TREDSOL", "TREDFRS")
var$colours <- c("red", "blue", "orange", "lightblue")
var$graph_type <- "bar"
var$labels_EN <- c("drought", "oxygen", "salinity", "frost")
var$labels_NL <- c("droogte", "zuurstof", "zout", "vorst")
var$y_label_EN <- "transpiration"
var$y_label_NL <- "transpiratie"
var$unit <- "mm"
var$factor <- 10
lstvar$TRED_PLOT <- var

# RAIN_IRRIG_PLOT
var <- list()
var$type <- "time"
var$variable <- c("RAIN", "IRRIG")
var$variable_optional <- c("IRRIG")
var$variable_type <- "rate"
var$levels <- c("IRRIG", "RAIN")
var$colours <- c("lightblue", "dodgerblue3")
var$graph_type <- "bar"
var$labels_EN <- c("irrigation", "precipitation")
var$labels_NL <- c("irrigatie", "neerslag")
var$y_label_EN <- "precipitation"
var$y_label_NL <- "neerslag"
var$unit <- "mm"
var$factor <- 10
lstvar$RAIN_IRRIG_PLOT <- var

# GWL
var <- list()
var$type <- "time"
var$variable <- "GWL"
var$variable_type <- "state"
var$nodata <- 999
var$colour <- "blue"
var$graph_type <- "line"
var$labels_EN <- "phreatic"
var$labels_NL <- "freatisch"
var$y_label_EN <- "groundwater level"
var$y_label_NL <- "grondwaterstand"
var$unit_EN <- "cm + sl"
var$unit_NL <- "cm + mv"
lstvar$GWL <- var

# RAIN
var <- list()
var$type <- "time"
var$variable <- "RAIN"
var$variable_type <- "rate"
var$colour <- "blue"
var$graph_type <- "bar"
var$labels_EN <- "precipitation"
var$labels_NL <- "neerslag"
var$y_label_EN <- "precipitation"
var$y_label_NL <- "neerslag"
var$unit <- "mm"
var$factor <- 10
lstvar$RAIN <- var

# RAIN_NET
var <- list()
var$type <- "time"
var$variable <- "RAIN_NET"
var$variable_type <- "rate"
var$colour <- "blue"
var$graph_type <- "bar"
var$labels_EN <- "net precipitation"
var$labels_NL <- "netto neerslag"
var$y_label_EN <- "net precipitation"
var$y_label_NL <- "netto neerslag"
var$unit <- "mm"
var$factor <- 10
lstvar$RAIN_NET <- var

# SNOW
var <- list()
var$type <- "time"
var$variable <- "SNOW"
var$variable_type <- "rate"
var$colour <- "wheat"
var$graph_type <- "bar"
var$labels_EN <- "snow"
var$labels_NL <- "sneeuw"
var$y_label_EN <- "snow"
var$y_label_NL <- "sneeuw"
var$unit <- "mm"
var$factor <- 10
lstvar$SNOW <- var

# RUNOFF
var <- list()
var$type <- "time"
var$variable <- "RUNOFF"
var$variable_type <- "rate"
var$colour <- "blue"
var$graph_type <- "bar"
var$labels_EN <- "runoff"
var$labels_NL <- "opp. afstroming"
var$y_label_EN <- "runoff"
var$y_label_NL <- "oppervlakkige afstroming"
var$unit <- "mm"
var$factor <- 10
lstvar$RUNOFF <- var

# RUNON
var <- list()
var$type <- "time"
var$variable <- "RUNON"
var$variable_type <- "rate"
var$colour <- "blue"
var$graph_type <- "line"
var$labels_EN <- "runon"
var$labels_NL <- "opp. aanstroming"
var$y_label_EN <- "runon"
var$y_label_NL <- "oppervlakkige aanstroming"
var$unit <- "mm"
var$factor <- 10
lstvar$RUNON <- var

# IRRIG
var <- list()
var$type <- "time"
var$variable <- "IRRIG"
var$variable_type <- "rate"
var$colour <- "lightblue"
var$graph_type <- "bar"
var$labels_EN <- "irrigation"
var$labels_NL <- "irrigatie"
var$y_label_EN <- "irrigation"
var$y_label_NL <- "irrigatie"
var$unit <- "mm"
var$factor <- 10
lstvar$IRRIG <- var

# INTERC
var <- list()
var$type <- "time"
var$variable <- "INTERC"
var$variable_type <- "rate"
var$colour <- "blue"
var$graph_type <- "bar"
var$labels_EN <- "interception"
var$labels_NL <- "interceptie"
var$y_labels_EN <- "interception"
var$y_labels_NL <- "interceptie"
var$unit <- "mm"
var$factor <- 10
lstvar$INTERC <- var

# TPOT
var <- list()
var$type <- "time"
var$variable <- "TPOT"
var$variable_type <- "rate"
var$colour <- "blue"
var$graph_type <- "bar"
var$labels_EN <- "potential"
var$labels_NL <- "potentieel"
var$y_label_EN <- "transpiration"
var$y_label_NL <- "transpiratie"
var$unit <- "mm"
var$factor <- 10
lstvar$TPOT <- var

# TACT
var <- list()
var$type <- "time"
var$variable <- "TACT"
var$variable_type <- "rate"
var$colour <- "blue"
var$graph_type <- "bar"
var$labels_EN <- "actual"
var$labels_NL <- "actueel"
var$y_label_EN <- "transpiration"
var$y_label_NL <- "transpiratie"
var$unit <- "mm"
var$factor <- 10
lstvar$TACT <- var

# EPOT
var <- list()
var$type <- "time"
var$variable <- "EPOT"
var$variable_type <- "rate"
var$colour <- "blue"
var$graph_type <- "bar"
var$labels_EN <- "potential"
var$labels_NL <- "potentieel"
var$y_label_EN <- "evaporation"
var$y_label_NL <- "evaporatie"
var$unit <- "mm"
var$factor <- 10
lstvar$EPOT <- var

# EACT
var <- list()
var$type <- "time"
var$variable <- "EACT"
var$variable_type <- "rate"
var$colour <- "blue"
var$graph_type <- "bar"
var$labels_EN <- "actual"
var$labels_NL <- "actueel"
var$y_label_EN <- "evaporation"
var$y_label_NL <- "evaporatie"
var$unit <- "mm"
var$factor <- 10
lstvar$EACT <- var

# ETPOT
var <- list()
var$type <- "time"
var$variable <- c("INTERC", "TPOT", "EPOT")
var$variable_type <- "rate"
var$colour <- "blue"
var$graph_type <- "bar"
var$labels_EN <- "potential"
var$labels_NL <- "potentieel"
var$y_label_EN <- "evapotranspiration"
var$y_label_NL <- "evapotranspiratie"
var$unit <- "mm"
var$factor <- 10
var$expression <- "INTERC + TPOT + EPOT"
lstvar$ETPOT <- var

# ETACT
var <- list()
var$type <- "time"
var$variable <- c("INTERC", "TACT", "EACT")
var$variable_type <- "rate"
var$colour <- "blue"
var$graph_type <- "bar"
var$labels_EN <- "actual"
var$labels_NL <- "actueel"
var$y_label_EN <- "evapotranspiration"
var$y_label_NL <- "evapotranspiratie"
var$unit <- "mm"
var$factor <- 10
var$expression <- "INTERC + TACT + EACT"
lstvar$ETACT <- var

# TREDDRY
var <- list()
var$type <- "time"
var$variable <- "TREDDRY"
var$variable_type <- "rate"
var$colour <- "red"
var$graph_type <- "bar"
var$labels_EN <- "drought stress"
var$labels_NL <- "droogtestress"
var$y_label_EN <- "transpiration reduction"
var$y_label_NL <- "transpiratiereductie"
var$unit <- "mm"
var$factor <- 10
lstvar$TREDDRY <- var

# TREDWET
var <- list()
var$type <- "time"
var$variable <- "TREDWET"
var$variable_type <- "rate"
var$colour <- "blue"
var$graph_type <- "bar"
var$labels_EN <- "oxygen stress"
var$labels_NL <- "zuurstofstress"
var$y_label_EN <- "transpiration reduction"
var$y_label_NL <- "transpiratiereductie"
var$unit <- "mm"
var$factor <- 10
lstvar$TREDWET <- var

# TREDSOL
var <- list()
var$type <- "time"
var$variable <- "TREDSOL"
var$variable_type <- "rate"
var$colour <- "orange"
var$graph_type <- "bar"
var$labels_EN <- "salinity stress"
var$labels_NL <- "zoutstress"
var$y_label_EN <- "transpiration reduction"
var$y_label_NL <- "transpiratiereductie"
var$unit <- "mm"
var$factor <- 10
lstvar$TREDSOL <- var

# TREDFRS
var <- list()
var$type <- "time"
var$variable <- "TREDFRS"
var$variable_type <- "rate"
var$colour <- "lighblue"
var$graph_type <- "bar"
var$labels_EN <- "frost stress"
var$labels_NL <- "vorststress"
var$y_label_EN <- "transpiration reduction"
var$y_label_NL <- "transpiratiereductie"
var$unit <- "mm"
var$factor <- 10
lstvar$TREDFRS <- var

# PP
var <- list()
var$type <- "time"
var$variable <- "PP"
var$variable_type <- "state"
var$colour <- "darkgreen"
var$graph_type <- "line"
var$labels_EN <- "root system"
var$labels_NL <- "wortelstelsel"
var$y_label_EN <- "pressure head"
var$y_label_NL <- "drukhoogte"
var$unit <- "cm"
var$factor <- -1
lstvar$PP <- var

# PL
var <- list()
var$type <- "time"
var$variable <- "PL"
var$variable_type <- "state"
var$colour <- "darkgreen"
var$graph_type <- "line"
var$labels_EN <- "leaves"
var$labels_NL <- "blad"
var$y_label_EN <- "pressure head"
var$y_label_NL <- "drukhoogte"
var$unit <- "cm"
var$factor <- -1
lstvar$PL <- var

# DRAINAGE
var <- list()
var$type <- "time"
var$variable <- "DRAINAGE"
var$variable_type <- "rate"
var$colour <- "blue"
var$graph_type <- "bar"
var$labels_EN <- "net drainage"
var$labels_NL <- "netto drainage"
var$y_label_EN <- "net drainage"
var$y_label_NL <- "netto drainage"
var$unit <- "mm"
var$factor <- 10
lstvar$DRAINAGE <- var

# DRAINAGE_1
var <- list()
var$type <- "time"
var$variable <- "DRAINAGE_1"
var$variable_type <- "rate"
var$colour <- "blue"
var$graph_type <- "bar"
var$labels_EN <- "drainage"
var$labels_NL <- "drainage"
var$y_label_EN <- "net drainage (sys 1)"
var$y_label_NL <- "netto drainage (sys 1)"
var$unit <- "mm"
var$factor <- 10
lstvar$DRAINAGE_1 <- var

# DRAINAGE_2
var <- list()
var$type <- "time"
var$variable <- "DRAINAGE_2"
var$variable_type <- "rate"
var$colour <- "blue"
var$graph_type <- "bar"
var$labels_EN <- "drainage"
var$labels_NL <- "drainage"
var$y_label_EN <- "net drainage (sys 2)"
var$y_label_NL <- "netto drainage (sys 2)"
var$unit <- "mm"
var$factor <- 10
lstvar$DRAINAGE_2 <- var

# DRAINAGE_3
var <- list()
var$type <- "time"
var$variable <- "DRAINAGE_3"
var$variable_type <- "rate"
var$colour <- "blue"
var$graph_type <- "bar"
var$labels_EN <- "drainage"
var$labels_NL <- "drainage"
var$y_label_EN <- "net drainage (sys 3)"
var$y_label_NL <- "netto drainage (sys 3)"
var$unit <- "mm"
var$factor <- 10
lstvar$DRAINAGE_3 <- var

# DRAINAGE_4
var <- list()
var$type <- "time"
var$variable <- "DRAINAGE_4"
var$variable_type <- "rate"
var$colour <- "blue"
var$graph_type <- "bar"
var$labels_EN <- "drainage"
var$labels_NL <- "drainage"
var$y_label_EN <- "net drainage (sys 4)"
var$y_label_NL <- "netto drainage (sys 4)"
var$unit <- "mm"
var$factor <- 10
lstvar$DRAINAGE_4 <- var

# DRAINAGE_5
var <- list()
var$type <- "time"
var$variable <- "DRAINAGE_5"
var$variable_type <- "rate"
var$colour <- "blue"
var$graph_type <- "bar"
var$labels_EN <- "drainage"
var$labels_NL <- "drainage"
var$y_label_EN <- "net drainage (sys 5)"
var$y_label_NL <- "netto drainage (sys 5)"
var$unit <- "mm"
var$factor <- 10
lstvar$DRAINAGE_5 <- var

# QBOTTOM
var <- list()
var$type <- "time"
var$variable <- "QBOTTOM"
var$variable_type <- "rate"
var$colour <- "blue"
var$graph_type <- "line"
var$labels_EN <- "bottom flux"
var$labels_NL <- "onderrand flux"
var$y_label_EN <- "bottom flux"
var$y_label_NL <- "onderrand flux"
var$unit <- "mm"
var$factor <- 10
lstvar$QBOTTOM <- var

# DSTOR
var <- list()
var$type <- "time"
var$variable <- "DSTOR"
var$variable_type <- "rate"
var$colour <- "blue"
var$graph_type <- "line"
var$labels_EN <- "change storage"
var$labels_NL <- "verandering berging"
var$y_label_EN <- "change storage"
var$y_label_NL <- "verandering berging"
var$unit <- "mm"
var$factor <- 10
lstvar$DSTOR <- var

# VOLACT
var <- list()
var$type <- "time"
var$variable <- "VOLACT"
var$variable_type <- "state"
var$colour <- "blue"
var$graph_type <- "bar"
var$labels_EN <- "storage"
var$labels_NL <- "berging"
var$y_label_EN <- "storage"
var$y_label_NL <- "berging"
var$unit <- "mm"
var$factor <- 10
lstvar$VOLACT <- var

# POND
var <- list()
var$type <- "time"
var$variable <- "POND"
var$variable_type <- "state"
var$colour <- "blue"
var$graph_type <- "bar"
var$labels_EN <- "ponding height"
var$labels_NL <- "ponding hoogte"
var$y_label_EN <- "ponding"
var$y_label_NL <- "ponding"
var$unit <- "mm"
var$factor <- 10
lstvar$POND <- var

# SSNOW
var <- list()
var$type <- "time"
var$variable <- "SSNOW"
var$variable_type <- "state"
var$colour <- "wheat"
var$graph_type <- "bar"
var$labels_EN <- "amount of snow"
var$labels_NL <- "sneeuwhoogte"
var$y_label_EN <- "snow"
var$y_label_NL <- "sneeuw"
var$unit <- "cm"
lstvar$SSNOW <- var

## TREL
#var <- list()
#var$variable <- c("TACT", "TPOT")
#var$parameter <- "Trel"
#var$name <- "Relative transpiration"
#var$longname <- "Relative transpiration"
#var$unit <- "-"
#var$expression <- "TACT / TPOT"
#var$NA_replace <- 1
#lstvar$TREL <- var

# # TREL (TRELDRY)
# var <- list()
# var$variable <- c("TREDDRY", "TPOT")
# var$parameter <- "Trel"
# var$name <- "Inverse relative transpiration caused by drought stress"
# var$longname <- "Inverse relative transpiration caused by drought stress"
# var$unit <- "-"
# var$expression <- "TREDDRY / TPOT"
# var$NA_replace <- 0
# lstvar$TREL <- var

# # TRELDRY
# var <- list()
# var$variable <- c("TREDDRY", "TPOT")
# var$parameter <- "Treldry"
# var$name <- "Inverse relative transpiration caused by drought stress"
# var$longname <- "Inverse relative transpiration caused by drought stress"
# var$unit <- "-"
# var$expression <- "TREDDRY / TPOT"
# var$NA_replace <- 0
# lstvar$TRELDRY <- var

# # TRELWET
# var <- list()
# var$variable <- c("TREDWET", "TPOT")
# var$parameter <- "Trelwet"
# var$name <- "Inverse relative transpiration caused by oxygen stress"
# var$longname <- "Innverse relative transpiration caused by oxygen stress"
# var$unit <- "-"
# var$expression <- "TREDWET / TPOT"
# var$NA_replace <- 0
# lstvar$TRELWET <- var

# # ASW
# var <- list()
# var$variable <- "WTOT[depth]"
# var$variable_input <- "WPF[depth]"
# var$parameter <- "S01"
# var$depth <- "-0:-30"
# var$pF <- 4.2
# var$name <- "Available soil water"
# var$longname <- "Available soil water 0-30cm"
# var$limit <- c(0, NA)
# var$unit <- "m"
# var$factor <- 0.01
# var$expression <- "WTOT - WPF"
# lstvar$ASW <- var

# # ASTO
# var <- list()
# var$variable <- "WTOT[depth]"
# var$variable_input <- "WPF[depth]"
# var$parameter <- "Ssd01"
# var$depth <- "-0:-30"
# var$pF <- 2.0
# var$name <- "Available storage"
# var$longname <- "Available storage 0-30cm"
# var$limit <- c(0, NA)
# var$unit <- "m"
# var$factor <- 0.01
# var$expression <- "WPF - WTOT"
# lstvar$ASTO <- var

# ---- WOFOST ----

# TSUM
var <- list()
var$type <- "time"
var$variable <- "TSUM"
var$variable_type <- "state"
var$colour <- "darkred"
var$graph_type <- "line"
var$labels_EN <- "temperature sum"
var$labels_NL <- "temperatuursom"
var$y_label_EN <- "temperature"
var$y_label_NL <- "temperatuur"
var$unit <- "oC"
lstvar$TSUM <- var

# DVS
var <- list()
var$type <- "time"
var$variable <- "DVS"
var$variable_type <- "state"
var$colour <- "green"
var$graph_type <- "line"
var$labels_EN <- "development stage"
var$labels_NL <- "ontwikkelingstadium"
var$y_label_EN <- "development stage"
var$y_label_NL <- "ontwikkelingstadium"
var$unit <- "-"
lstvar$DVS <- var

# HEIGTH
var <- list()
var$type <- "time"
var$variable <- "HEIGTH"
var$variable_type <- "state"
var$colour <- "green"
var$graph_type <- "line"
var$labels_EN <- "crop height"
var$labels_NL <- "gewashoogte"
var$y_label_EN <- "crop height"
var$y_label_NL <- "gewashoogte"
var$unit <- "cm"
lstvar$HEIGTH <- var

# CRPFAC
var <- list()
var$type <- "time"
var$variable <- "CRPFAC"
var$variable_type <- "state"
var$colour <- "green"
var$graph_type <- "line"
var$labels_EN <- "crop factor"
var$labels_NL <- "gewasfactor"
var$y_label_EN <- "factor"
var$y_label_NL <- "factor"
var$unit <- "-"
lstvar$CRPFAC <- var

# PGASSPOT
var <- list()
var$deprecated <- "4.2.150"
var$type <- "time"
var$variable <- "PGASSPOT"
var$variable_type <- "rate"
var$colour <- "black"
var$graph_type <- "bar"
var$labels_EN <- "potential"
var$labels_NL <- "potentieel"
var$y_label_EN <- "assimilation rate"
var$y_label_NL <- "assimilatie"
var$unit <- "kgch ha-1"
lstvar$PGASSPOT <- var

# GASSTPOT
var <- list()
var$type <- "time"
var$variable <- "GASSTPOT"
var$variable_type <- "rate"
var$colour <- "black"
var$graph_type <- "bar"
var$labels_EN <- "potential"
var$labels_NL <- "potentieel"
var$y_label_EN <- "assimilation rate"
var$y_label_NL <- "assimilatie"
var$unit <- "kgch ha-1"
lstvar$GASSTPOT <- var

# PGASS
var <- list()
var$deprecated <- "4.2.150"
var$type <- "time"
var$variable <- "PGASS"
var$variable_type <- "rate"
var$colour <- "green"
var$graph_type <- "bar"
var$labels_EN <- "actual"
var$labels_NL <- "actueel"
var$y_label_EN <- "assimilation rate"
var$y_label_NL <- "assimilatie"
var$unit <- "kgch ha-1"
lstvar$PGASS <- var

# GASST
var <- list()
var$deprecated <- "4.2.150"
var$type <- "time"
var$variable <- "PGASS"
var$variable_type <- "rate"
var$colour <- "green"
var$graph_type <- "bar"
var$labels_EN <- "actual"
var$labels_NL <- "actueel"
var$y_label_EN <- "assimilation rate"
var$y_label_NL <- "assimilatie"
var$unit <- "kgch ha-1"
lstvar$PGASST <- var

# MRESTPOT
var <- list()
var$type <- "time"
var$variable <- "RESTPOT"
var$variable_type <- "rate"
var$colour <- "black"
var$graph_type <- "bar"
var$labels_EN <- "potential"
var$labels_NL <- "potentieel"
var$y_label_EN <- "maintenance respiration"
var$y_label_NL <- "onderhoudsademhaling"
var$unit <- "kgch ha-1"
lstvar$MRESTPOT <- var

# MREST
var <- list()
var$type <- "time"
var$variable <- "REST"
var$variable_type <- "rate"
var$colour <- "green"
var$graph_type <- "bar"
var$labels_EN <- "actual"
var$labels_NL <- "actueel"
var$y_label_EN <- "maintenance respiration"
var$y_label_NL <- "onderhoudsademhaling"
var$unit <- "kgch ha-1"
lstvar$MREST <- var

# CPWDM
var <- list()
var$deprecated <- "4.2.150"
var$type <- "time"
var$variable <- "CPWDM"
var$variable_type <- "state"
var$colour <- "black"
var$graph_type <- "line"
var$labels_EN <- "potential"
var$labels_NL <- "potentieel"
var$y_label_EN <- "aboveground biomass"
var$y_label_NL <- "bovengrondse biomassa"
var$unit <- "kgds ha-1"
lstvar$CPWDM <- var

# PWDM
var <- list()
var$type <- "time"
var$variable <- "PWDM"
var$variable_type <- "state"
var$colour <- "black"
var$graph_type <- "line"
var$labels_EN <- "potential"
var$labels_NL <- "potentieel"
var$y_label_EN <- "aboveground biomass"
var$y_label_NL <- "bovengrondse biomassa"
var$unit <- "kgds ha-1"
lstvar$PWDM <- var

# CWDM
var <- list()
var$deprecated <- "4.2.150"
var$type <- "time"
var$variable <- "CWDM"
var$variable_type <- "state"
var$colour <- "green"
var$graph_type <- "line"
var$labels_EN <- "actual"
var$labels_NL <- "actueel"
var$y_label_EN <- "aboveground biomass"
var$y_label_NL <- "bovengrondse biomassa"
var$unit <- "kgds ha-1"
lstvar$CWDM <- var

# WDM
var <- list()
var$type <- "time"
var$variable <- "WDM"
var$variable_type <- "state"
var$colour <- "green"
var$graph_type <- "line"
var$labels_EN <- "actual"
var$labels_NL <- "actueel"
var$y_label_EN <- "aboveground biomass"
var$y_label_NL <- "bovengrondse biomassa"
var$unit <- "kgds ha-1"
lstvar$WDM <- var

# CPWSO
var <- list()
var$deprecated <- "4.2.150"
var$type <- "time"
var$variable <- "CPWSO"
var$variable_type <- "state"
var$colour <- "black"
var$graph_type <- "line"
var$labels_EN <- "potential"
var$labels_NL <- "potentieel"
var$y_label_EN <- "weight storage organs"
var$y_label_NL <- "biomassa vrucht"
var$unit <- "kgds ha-1"
lstvar$CPWSO <- var

# PWSO
var <- list()
var$type <- "time"
var$variable <- "PWSO"
var$variable_type <- "state"
var$colour <- "black"
var$graph_type <- "line"
var$labels_EN <- "potential"
var$labels_NL <- "potentieel"
var$y_label_EN <- "weight storage organs"
var$y_label_NL <- "biomassa vrucht"
var$unit <- "kgds ha-1"
lstvar$PWSO <- var

# CWSO
var <- list()
var$deprecated <- "4.2.150"
var$type <- "time"
var$variable <- "CWSO"
var$variable_type <- "state"
var$colour <- "green"
var$graph_type <- "line"
var$labels_EN <- "actual"
var$labels_NL <- "actueel"
var$y_label_EN <- "weight storage organs"
var$y_label_NL <- "gewicht vrucht"
var$unit <- "kgds ha-1"
lstvar$CWSO <- var

# WSO
var <- list()
var$type <- "time"
var$variable <- "WSO"
var$variable_type <- "state"
var$colour <- "green"
var$graph_type <- "line"
var$labels_EN <- "actual"
var$labels_NL <- "actueel"
var$y_label_EN <- "weight storage organs"
var$y_label_NL <- "gewicht vrucht"
var$unit <- "kgds ha-1"
lstvar$WSO <- var

# PWLV
var <- list()
var$type <- "time"
var$variable <- "PWLV"
var$variable_type <- "state"
var$colour <- "black"
var$graph_type <- "line"
var$labels_EN <- "potential"
var$labels_NL <- "potentieel"
var$y_label_EN <- "weight green leaves"
var$y_label_NL <- "gewicht groene bladeren"
var$unit <- "kgds ha-1"
lstvar$PWLV <- var

# PDWLV
var <- list()
var$type <- "time"
var$variable <- "PDWLV"
var$variable_type <- "state"
var$colour <- "darkgoldenrod4"
var$graph_type <- "line"
var$labels_EN <- "potential"
var$labels_NL <- "potentieel"
var$y_label_EN <- "weight dead leaves"
var$y_label_NL <- "gewicht dode bladeren"
var$unit <- "kgds ha-1"
lstvar$PDWLV <- var

# PTWLV
var <- list()
var$type <- "time"
var$variable <- "PTWLV"
var$variable_type <- "state"
var$colour <- "black"
var$graph_type <- "line"
var$labels_EN <- "potential"
var$labels_NL <- "potentieel"
var$y_label_EN <- "total weight leaves"
var$y_label_NL <- "tot. gewicht bladeren"
var$unit <- "kgds ha-1"
lstvar$PTWLV <- var

# WLV
var <- list()
var$type <- "time"
var$variable <- "WLV"
var$variable_type <- "state"
var$colour <- "green"
var$graph_type <- "line"
var$labels_EN <- "actual"
var$labels_NL <- "actueel"
var$y_label_EN <- "weight green leaves"
var$y_label_NL <- "gewicht groene bladeren"
var$unit <- "kgds ha-1"
lstvar$WLV <- var

# DWLV
var <- list()
var$type <- "time"
var$variable <- "DWLV"
var$variable_type <- "state"
var$colour <- "darkgoldenrod2"
var$graph_type <- "line"
var$labels_EN <- "actual"
var$labels_NL <- "actueel"
var$y_label_EN <- "weight dead leaves"
var$y_label_NL <- "gewicht dode bladeren"
var$unit <- "kgds ha-1"
lstvar$DWLV <- var

# TWLV
var <- list()
var$type <- "time"
var$variable <- "TWLV"
var$variable_type <- "state"
var$colour <- "green"
var$graph_type <- "line"
var$labels_EN <- "actual"
var$labels_NL <- "actueel"
var$y_label_EN <- "total weight leaves"
var$y_label_NL <- "tot. gewicht bladeren"
var$unit <- "kgds ha-1"
lstvar$TWLV <- var

# PWST
var <- list()
var$type <- "time"
var$variable <- "PWST"
var$variable_type <- "state"
var$colour <- "black"
var$graph_type <- "line"
var$labels_EN <- "potential"
var$labels_NL <- "potentieel"
var$y_label_EN <- "weight stems"
var$y_label_NL <- "gewicht stengels"
var$unit <- "kgds ha-1"
lstvar$PWST <- var

# PDWST
var <- list()
var$type <- "time"
var$variable <- "PDWST"
var$variable_type <- "state"
var$colour <- "darkgoldenrod4"
var$graph_type <- "line"
var$labels_EN <- "potential"
var$labels_NL <- "potentieel"
var$y_label_EN <- "weight dead stems"
var$y_label_NL <- "gewicht dode stengels"
var$unit <- "kgds ha-1"
lstvar$PDWST <- var

# PTWST
var <- list()
var$type <- "time"
var$variable <- "PTWST"
var$variable_type <- "state"
var$colour <- "black"
var$graph_type <- "line"
var$labels_EN <- "potential"
var$labels_NL <- "potentieel"
var$y_label_EN <- "total weight stems"
var$y_label_NL <- "tot. gewicht stengels"
var$unit <- "kgds ha-1"
lstvar$PTWST <- var

# WST
var <- list()
var$type <- "time"
var$variable <- "WST"
var$variable_type <- "state"
var$colour <- "green"
var$graph_type <- "line"
var$labels_EN <- "actual"
var$labels_NL <- "actueel"
var$y_label_EN <- "weight stems"
var$y_label_NL <- "gewicht stengels"
var$unit <- "kgds ha-1"
lstvar$WST <- var

# DWST
var <- list()
var$type <- "time"
var$variable <- "DWST"
var$variable_type <- "state"
var$colour <- "darkgoldenrod2"
var$graph_type <- "line"
var$labels_EN <- "actual"
var$labels_NL <- "actueel"
var$y_label_EN <- "weight dead stems"
var$y_label_NL <- "gewicht dode stengels"
var$unit <- "kgds ha-1"
lstvar$DWST <- var

# TWST
var <- list()
var$type <- "time"
var$variable <- "TWST"
var$variable_type <- "state"
var$colour <- "green"
var$graph_type <- "line"
var$labels_EN <- "actual"
var$labels_NL <- "actueel"
var$y_label_EN <- "total weight stems"
var$y_label_NL <- "tot. gewicht stengels"
var$unit <- "kgds ha-1"
lstvar$DWST <- var

# PWRT
var <- list()
var$type <- "time"
var$variable <- "PWRT"
var$variable_type <- "state"
var$colour <- "black"
var$graph_type <- "line"
var$labels_EN <- "potential"
var$labels_NL <- "potentieel"
var$y_label_EN <- "weight roots"
var$y_label_NL <- "gewicht wortels"
var$unit <- "kgds ha-1"
lstvar$PWRT <- var

# PDWRT
var <- list()
var$type <- "time"
var$variable <- "PDWRT"
var$variable_type <- "state"
var$colour <- "darkgoldenrod4"
var$graph_type <- "line"
var$labels_EN <- "potential"
var$labels_NL <- "potentieel"
var$y_label_EN <- "weight dead roots"
var$y_label_NL <- "gewicht dode wortels"
var$unit <- "kgds ha-1"
lstvar$PDWRT <- var

# PTWRT
var <- list()
var$type <- "time"
var$variable <- "PTWRT"
var$variable_type <- "state"
var$colour <- "black"
var$graph_type <- "line"
var$labels_EN <- "potential"
var$labels_NL <- "potentieel"
var$y_label_EN <- "total weight roots"
var$y_label_NL <- "tot. gewicht wortels"
var$unit <- "kgds ha-1"
lstvar$PTWRT <- var

# WRT
var <- list()
var$type <- "time"
var$variable <- "WRT"
var$variable_type <- "state"
var$colour <- "green"
var$graph_type <- "line"
var$labels_EN <- "actual"
var$labels_NL <- "actueel"
var$y_label_EN <- "weight roots"
var$y_label_NL <- "gewicht wortels"
var$unit <- "kgds ha-1"
lstvar$WRT <- var

# DWRT
var <- list()
var$type <- "time"
var$variable <- "DWRT"
var$variable_type <- "state"
var$colour <- "darkgoldenrod2"
var$graph_type <- "line"
var$labels_EN <- "actual"
var$labels_NL <- "actueel"
var$y_label_EN <- "weight dead roots"
var$y_label_NL <- "gewicht dode wortels"
var$unit <- "kgds ha-1"
lstvar$DWRT <- var

# TWRT
var <- list()
var$type <- "time"
var$variable <- "TWRT"
var$variable_type <- "state"
var$colour <- "green"
var$graph_type <- "line"
var$labels_EN <- "actual"
var$labels_NL <- "actueel"
var$y_label_EN <- "total weight roots"
var$y_label_NL <- "tot. gewicht wortels"
var$unit <- "kgds ha-1"
lstvar$TWRT <- var

# DWLVPOT
var <- list()
var$depreacated <- "4.2.147"
var$type <- "time"
var$variable <- "DWLVPOT"
var$variable_type <- "state"
var$colour <- "darkgoldenrod4"
var$graph_type <- "line"
var$labels_EN <- "potential"
var$labels_NL <- "potentieel"
var$y_label_EN <- "dead weight leaves"
var$y_label_NL <- "dood gewicht bladeren"
var$unit <- "kgds ha-1"
lstvar$DWLVPOT <- var

# DWSTPOT
var <- list()
var$depreacated <- "4.2.147"
var$type <- "time"
var$variable <- "DWSTPOT"
var$variable_type <- "state"
var$colour <- "darkgoldenrod4"
var$graph_type <- "line"
var$labels_EN <- "potential"
var$labels_NL <- "potentieel"
var$y_label_EN <- "dead weight stems"
var$y_label_NL <- "dood gewicht stengels"
var$unit <- "kgds ha-1"
lstvar$DWSTPOT <- var

# DWRTPOT
var <- list()
var$depreacated <- "4.2.147"
var$type <- "time"
var$variable <- "DWRTPOT"
var$variable_type <- "state"
var$colour <- "darkgoldenrod4"
var$graph_type <- "line"
var$labels_EN <- "potential"
var$labels_NL <- "potentieel"
var$y_label_EN <- "dead weight roots"
var$y_label_NL <- "dood gewicht wortels"
var$unit <- "kgds ha-1"
lstvar$DWRTPOT <- var

# PGRASSDM
var <- list()
var$depreacated <- "4.2.150"
var$type <- "time"
var$variable <- "PGRASSDM"
var$variable_type <- "state"
var$colour <- "black"
var$graph_type <- "line"
var$labels_EN <- "potential"
var$labels_NL <- "potentieel"
var$y_label_EN <- "aboveground biomass"
var$y_label_NL <- "bovengrondse biomassa"
var$unit <- "kgds ha-1"
lstvar$PGRASSDM <- var

# GRASSDM
var <- list()
var$depreacated <- "4.2.150"
var$type <- "time"
var$variable <- "GRASSDM"
var$variable_type <- "state"
var$colour <- "green"
var$graph_type <- "line"
var$labels_EN <- "actual"
var$labels_NL <- "actueel"
var$y_label_EN <- "aboveground biomass"
var$y_label_NL <- "bovengrondse biomassa"
var$unit <- "kgds ha-1"
lstvar$GRASSDM <- var

# PMOWDM
var <- list()
var$depreacated <- "4.2.150"
var$type <- "time"
var$variable <- "PMOWDM"
var$variable_type <- "state"
var$colour <- "black"
var$graph_type <- "line"
var$labels_EN <- "potential"
var$labels_NL <- "potentieel"
var$y_label_EN <- "harvested weight by mowing"
var$y_label_NL <- "geoogst gewicht maaien"
var$unit <- "kgds ha-1"
lstvar$PMOWDM <- var

# MOWDM
var <- list()
var$depreacated <- "4.2.150"
var$type <- "time"
var$variable <- "MOWDM"
var$variable_type <- "state"
var$colour <- "green"
var$graph_type <- "line"
var$labels_EN <- "actual"
var$labels_NL <- "actueel"
var$y_label_EN <- "harvested weight by mowing"
var$y_label_NL <- "geoogst gewicht maaien"
var$unit <- "kgds ha-1"
lstvar$MOWDM <- var

# PGRAZDM
var <- list()
var$depreacated <- "4.2.150"
var$type <- "time"
var$variable <- "PGRAZDM"
var$variable_type <- "state"
var$colour <- "black"
var$graph_type <- "line"
var$labels_EN <- "potential"
var$labels_NL <- "potentieel"
var$y_label_EN <- "harvested weight by grazing"
var$y_label_NL <- "geoogst gewicht begrazing"
var$unit <- "kgds ha-1"
lstvar$PGRAZDM <- var

# GRAZDM
var <- list()
var$depreacated <- "4.2.150"
var$type <- "time"
var$variable <- "GRAZDM"
var$variable_type <- "state"
var$colour <- "green"
var$graph_type <- "line"
var$labels_EN <- "actual"
var$labels_NL <- "actueel"
var$y_label_EN <- "harvested weight by grazing"
var$y_label_NL <- "geoogst gewicht begrazing"
var$unit <- "kgds ha-1"
lstvar$GRAZDM <- var

# PHRVDM
var <- list()
var$type <- "time"
var$variable <- "PHRVDM"
var$variable_type <- "state"
var$colour <- "black"
var$graph_type <- "line"
var$labels_EN <- "potential"
var$labels_NL <- "potentieel"
var$y_label_EN <- "harvested weight"
var$y_label_NL <- "geoogst gewicht"
var$unit <- "kgds ha-1"
lstvar$PHRVDM <- var

# HRVDM
var <- list()
var$type <- "time"
var$variable <- "HRVDM"
var$variable_type <- "state"
var$colour <- "green"
var$graph_type <- "line"
var$labels_EN <- "actual"
var$labels_NL <- "actueel"
var$y_label_EN <- "harvested weight"
var$y_label_NL <- "geoogst gewicht"
var$unit <- "kgds ha-1"
lstvar$HRVDM <- var

# PLOSSDM
var <- list()
var$type <- "time"
var$variable <- "PLOSSDM"
var$variable_type <- "state"
var$colour <- "darkgoldenrod4"
var$graph_type <- "line"
var$labels_EN <- "potential"
var$labels_NL <- "potentieel"
var$y_label_EN <- "weight losses"
var$y_label_NL <- "gewicht verlies"
var$unit <- "kgds ha-1"
lstvar$PLOSSDM <- var

# LOSSDM
var <- list()
var$type <- "time"
var$variable <- "LOSSDM"
var$variable_type <- "state"
var$colour <- "darkgoldenrod3"
var$graph_type <- "line"
var$labels_EN <- "actual"
var$labels_NL <- "actueel"
var$y_label_EN <- "weight losses"
var$y_label_NL <- "gewicht verlies"
var$unit <- "kgds ha-1"
lstvar$LOSSDM <- var

# ICUTPOT
var <- list()
var$type <- "time"
var$variable <- "ICUTPOT"
var$variable_type <- "state"
var$colour <- "darkgoldenrod4"
var$graph_type <- "line"
var$labels_EN <- "potential"
var$labels_NL <- "potentieel"
var$y_label_EN <- "grass cut"
var$y_label_NL <- "grassnede"
var$unit <- "-"
lstvar$ICUTPOT <- var

# ICUT
var <- list()
var$type <- "time"
var$variable <- "ICUT"
var$variable_type <- "state"
var$colour <- "darkgoldenrod3"
var$graph_type <- "line"
var$labels_EN <- "actual"
var$labels_NL <- "actueel"
var$y_label_EN <- "grass cut"
var$y_label_NL <- "grassnede"
var$unit <- "-"
lstvar$ICUT <- var

# TCUTPOT
var <- list()
var$type <- "time"
var$variable <- "TCUTPOT"
var$variable_type <- "state"
var$colour <- "darkgoldenrod4"
var$graph_type <- "line"
var$labels_EN <- "potential"
var$labels_NL <- "potentieel"
var$y_label_EN <- "duration grass cut"
var$y_label_NL <- "duur grassnede"
var$unit <- "d"
lstvar$TCUTPOT <- var

# TCUT
var <- list()
var$type <- "time"
var$variable <- "TCUT"
var$variable_type <- "state"
var$colour <- "darkgoldenrod3"
var$graph_type <- "line"
var$labels_EN <- "actual"
var$labels_NL <- "actueel"
var$y_label_EN <- "duration grass cut"
var$y_label_NL <- "duur grassnede"
var$unit <- "-"
lstvar$TCUT <- var

# LAIPOT
var <- list()
var$type <- "time"
var$variable <- "LAIPOT"
var$variable_type <- "state"
var$colour <- "black"
var$graph_type <- "line"
var$labels_EN <- "potential"
var$labels_NL <- "potentieel"
var$y_label_EN <- "Leaf Area Index"
var$y_label_NL <- "Leaf Area Index"
var$unit <- "m2 m-2"
lstvar$LAIPOT <- var

# LAI
var <- list()
var$type <- "time"
var$variable <- "LAI"
var$variable_type <- "state"
var$colour <- "green"
var$graph_type <- "line"
var$labels_EN <- "actual"
var$labels_NL <- "actueel"
var$y_label_EN <- "Leaf Area Index"
var$y_label_NL <- "Leaf Area Index"
var$unit <- "m2 m-2"
lstvar$LAI <- var

# RDPOT
var <- list()
var$type <- "time"
var$variable <- "RDPOT"
var$variable_type <- "state"
var$colour <- "black"
var$graph_type <- "line"
var$labels_EN <- "potential"
var$labels_NL <- "potentieel"
var$y_label_EN <- "rooting depth"
var$y_label_NL <- "wortelzone"
var$unit <- "cm"
var$expression <- "-1 * RDPOT"
lstvar$RDPOT <- var

# RD
var <- list()
var$type <- "time"
var$variable <- "RD"
var$variable_type <- "state"
var$colour <- "green"
var$graph_type <- "line"
var$labels_EN <- "actual"
var$labels_NL <- "actueel"
var$y_label_EN <- "rooting depth"
var$y_label_NL <- "wortelzone"
var$unit <- "cm"
var$expression <- "-1 * RD"
lstvar$RD <- var

# ---- SOLUTES ----

# SOLBAL_PLOT
var <- list()
var$type <- "time"
var$variable <- c("SQPREC", "SQIRRIG", "SQDRA", "SQBOT", "SAMPRO", "ROTTOT", "DECTOT")
var$variable_optional <- c("SQBOT", "SQDRA", "ROTTOT", "DECTOT")
var$variable_type <- "rate"
var$levels <- c("SQPREC", "SQIRRIG", "SQDRA", "ROTTOT", "DECTOT", "DSAMPRO", "SQBOT")
var$colours <- c("dodgerblue3", "lightblue", "goldenrod4", "darkgreen", "sienna", "cornsilk3", "darkblue")
var$graph_type <- "bar"
var$labels_EN <- c("precipitation", "irrigation", "drainage", "root uptake", "decomposition", "change", "bottomflux")
var$labels_NL <- c("neerslag", "irrigatie", "drainage", "opname plant", "afbraak", "verandering", "onderrand")
var$y_label_EN <- "net solute balance"
var$y_label_NL <- "netto zoutbalans"
var$unit <- "g cm-2"
lstvar$SOLBAL_PLOT <- var

# SQPREC
var <- list()
var$type <- "time"
var$variable <- "SQPREC"
var$variable_type <- "rate"
var$colour <- "orange"
var$graph_type <- "line"
var$labels_EN <- "precipitation"
var$labels_NL <- "neerslag"
var$y_label_EN <- "solutes in precipitation"
var$y_label_NL <- "zout in neerslag"
var$unit <- "g cm-2"
lstvar$SQPREC <- var

# SQIRRIG
var <- list()
var$type <- "time"
var$variable <- "SQIRRIG"
var$variable_type <- "rate"
var$colour <- "orange"
var$graph_type <- "line"
var$labels_EN <- "irrigation"
var$labels_NL <- "irrigatie"
var$y_label_EN <- "solutes in irrigation"
var$y_label_NL <- "zout in irrigatie"
var$unit <- "g cm-2"
lstvar$SQIRRIG <- var

# SQBOT
var <- list()
var$type <- "time"
var$variable <- "SQBOT"
var$variable_type <- "rate"
var$colour <- "orange"
var$graph_type <- "line"
var$labels_EN <- "amount over bottom"
var$labels_NL <- "hoeveelheid onderrand"
var$y_label_EN <- "amount over bottom"
var$y_label_NL <- "hoeveelheid onderrand"
var$unit <- "g cm-2"
lstvar$SQBOT <- var

# SQDRA
var <- list()
var$type <- "time"
var$variable <- "SQDRA"
var$variable_type <- "rate"
var$colour <- "orange"
var$graph_type <- "line"
var$labels_EN <- "amount of drainage"
var$labels_NL <- "hoeveelheid drainage"
var$y_labels_EN <- "amount of drainage"
var$y_labels_NL <- "hoeveelheid drainage"
var$unit <- "g cm-2"
lstvar$SQDRA <- var

# DECTOT
var <- list()
var$type <- "time"
var$variable <- "DECTOT"
var$variable_type <- "rate"
var$colour <- "orange"
var$graph_type <- "line"
var$labels_EN <- "amount of decomposition"
var$labels_NL <- "hoeveelheid afbraak"
var$y_labels_EN <- "amount of decomposition"
var$y_labels_NL <- "hoeveelheid afbraak"
var$unit <- "g cm-2"
lstvar$DECTOT <- var

# ROTTOT
var <- list()
var$type <- "time"
var$variable <- "ROTTOT"
var$variable_type <- "rate"
var$colour <- "orange"
var$graph_type <- "line"
var$labels_EN <- "amount of uptake"
var$labels_NL <- "hoeveelheid opname"
var$y_labels_EN <- "amount of uptake"
var$y_labels_NL <- "hoeveelheid opname"
var$unit <- "g cm-2"
lstvar$ROTTOT <- var

# SAMPRO
var <- list()
var$type <- "time"
var$variable <- "SAMPRO"
var$variable_type <- "state"
var$colour <- "orange"
var$graph_type <- "line"
var$labels_EN <- "total solutes in profile"
var$labels_NL <- "tot. zout in profiel"
var$y_labels_EN <- "amount of solutes in profile"
var$y_labels_NL <- "hoeveelheid zout in profiel"
var$unit <- "g cm-2"
lstvar$SAMPRO <- var

# SOLERR
var <- list()
var$type <- "time"
var$variable <- "SOLERR"
var$variable_type <- "state"
var$colour <- "orange"
var$graph_type <- "bar"
var$labels_EN <- "error"
var$labels_NL <- "balansfout"
var$y_labels_EN <- "error in solute balance"
var$y_labels_NL <- "balansfout in zout"
var$unit <- "g cm-2"
lstvar$SOLACT <- var

# write rds
write_rds(x = lstvar, "swap_output.rds")
