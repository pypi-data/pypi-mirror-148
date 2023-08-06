from exchangeraterepo.repository.ExchangeRateRepository import ExchangeRateRepository
from oracle.resolve.PredictionResolver import PredictionResolver
from positionrepo.repository.PositionRepository import PositionRepository
from tradestrategy.TradeStrategyProcessor import TradeStrategyProcessor

from automata.exception.AutomataRequirementMissingException import AutomataRequirementMissingException


class Automata:

    def __init__(self, options):
        self.options = options
        # repositories
        self.position_repository: PositionRepository = None
        self.exchange_rate_repository: ExchangeRateRepository = None
        # required dependencies
        self.prediction_resolver: PredictionResolver = None
        self.trade_strategy_processor: TradeStrategyProcessor = None
        self.__init_in_sequence()

    def __init_in_sequence(self):
        self.init_repositories()
        self.init_prediction_resolver()
        self.init_trade_strategy_processor()

    def init_repositories(self):
        self.position_repository = PositionRepository(self.options)
        self.exchange_rate_repository = ExchangeRateRepository(self.options)

    def init_prediction_resolver(self):
        if self.prediction_resolver is None:
            raise AutomataRequirementMissingException('Prediction Resolver is required! Implement "init_prediction_resolver"')

    def init_trade_strategy_processor(self):
        if self.trade_strategy_processor is None:
            raise AutomataRequirementMissingException('Trade Strategy Processor is required! Implement "init_trade_strategy_processor"')

    def run(self):
        position = self.position_repository.retrieve()

        # todo: need exchangeable (instruments) + time frame
        exchange_rates = self.exchange_rate_repository.retrieve_multiple()

        prediction = self.prediction_resolver.resolve(position.instrument, exchange_rates)

        self.trade_strategy_processor.perform_trade(position, prediction)
