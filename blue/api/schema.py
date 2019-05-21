import graphene

from graphene_django.types import DjangoObjectType
from graphene_django.forms.mutation import DjangoModelFormMutation

from .forms import RegisterForm, RegisterRowForm, StatisticsForm, StatisticsRowRegisterForm, StatisticsRowStatisticsForm
from core.models import Register, RegisterRow, Statistics, StatisticsRowRegister, StatisticsRowStatistics, calculate_register_amount, calculate_statistics_result


class MeObject(graphene.ObjectType):
    username = graphene.String()


class RegisterType(DjangoObjectType):
    class Meta:
        model = Register

    amount = graphene.Float()

    def resolve_amount(self, args):
        return calculate_register_amount(self.id)


class RegisterRowType(DjangoObjectType):
    class Meta:
        model = RegisterRow


class StatisticsType(DjangoObjectType):
    class Meta:
        model = Statistics

    result = graphene.Float()

    def resolve_result(self, args):
        return calculate_statistics_result(self.id)


class RegisterMutation(DjangoModelFormMutation):
    class Meta:
        form_class = RegisterForm

    @classmethod
    def perform_mutate(cls, form, info):
        obj = form.save(commit=False)
        obj.user = info.context.user
        obj.save()
        kwargs = {cls._meta.return_field_name: obj}
        return cls(errors=[], **kwargs)


class RegisterRowMutation(DjangoModelFormMutation):
    class Meta:
        form_class = RegisterRowForm

    @classmethod
    def perform_mutate(cls, form, info):
        obj = form.save(commit=False)
        obj.user = info.context.user
        obj.save()
        kwargs = {cls._meta.return_field_name: obj}
        return cls(errors=[], **kwargs)


class StatisticsMutation(DjangoModelFormMutation):
    class Meta:
        form_class = StatisticsForm

    @classmethod
    def perform_mutate(cls, form, info):
        obj = form.save(commit=False)
        obj.user = info.context.user
        obj.save()
        kwargs = {cls._meta.return_field_name: obj}
        return cls(errors=[], **kwargs)


class RegisterDeleteMutation(graphene.Mutation):
    class Arguments:
        pk = graphene.Int()

    success = graphene.Boolean()

    def mutate(self, info, pk):

        Register.objects.filter(id=pk).delete()
        return RegisterDeleteMutation(success=True)


class RegisterRowDeleteMutation(graphene.Mutation):
    class Arguments:
        pk = graphene.Int()

    success = graphene.Boolean()

    def mutate(self, info, pk):

        RegisterRow.objects.filter(id=pk).delete()
        return RegisterRowDeleteMutation(success=True)


class StatisticsDeleteMutation(graphene.Mutation):
    class Arguments:
        pk = graphene.Int()

    success = graphene.Boolean()

    def mutate(self, info, pk):

        Statistics.objects.filter(id=pk).delete()
        return StatisticsDeleteMutation(success=True)


class Query(graphene.ObjectType):
    me = graphene.Field(MeObject)

    detail_register = graphene.Field(RegisterType, id=graphene.Int())
    detail_statistics = graphene.Field(StatisticsType, id=graphene.Int())
    detail_register_row = graphene.Field(RegisterRowType, id=graphene.Int())

    list_register = graphene.List(RegisterType)
    list_statistics = graphene.List(StatisticsType)

    def resolve_me(self, info, **kwargs):
        if info.context.user.is_authenticated:
            return MeObject(username=info.context.user.username)
        return None

    def resolve_detail_register(self, info, **kwargs):
        id = kwargs.get("id")
        if id is not None:
            return Register.objects.get(pk=id)
        return None

    def resolve_detail_register_row(self, info, **kwargs):
        id = kwargs.get("id")
        if id is not None:
            return RegisterRow.objects.get(pk=id)
        return None

    def resolve_detail_statistics(self, info, **kwargs):
        id = kwargs.get("id")
        if id is not None:
            return Statistics.objects.get(pk=id)
        return None

    def resolve_list_register(self, info, **kwargs):
        return Register.objects.filter(user=info.context.user)

    def resolve_list_register_row(self, info, **kwargs):
        return RegisterRow.objects.filter(user=info.context.user)

    def resolve_list_statistics(self, info, **kwargs):
        return Statistics.objects.filter(user=info.context.user)


class Mutations(graphene.ObjectType):
    mutation_register = RegisterMutation.Field()
    mutation_register_row = RegisterRowMutation.Field()
    mutation_statistics = StatisticsMutation.Field()

    mutation_delete_register = RegisterDeleteMutation.Field()
    mutation_delete_register_row = RegisterRowDeleteMutation.Field()
    mutation_delete_statistics = StatisticsDeleteMutation.Field()


schema = graphene.Schema(query=Query, mutation=Mutations)
