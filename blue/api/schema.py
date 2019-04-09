import graphene

from graphene_django.types import DjangoObjectType
from graphene_django.forms.mutation import DjangoModelFormMutation

from .forms import RegisterForm, ItemForm, StatisticsForm
from core.models import Register, Item, Statistics


class MeObject(graphene.ObjectType):
    username = graphene.String()


class RegisterType(DjangoObjectType):
    class Meta:
        model = Register


class ItemType(DjangoObjectType):
    class Meta:
        model = Item


class StatisticsType(DjangoObjectType):
    class Meta:
        model = Statistics


class CounterMutation(DjangoModelFormMutation):
    class Meta:
        form_class = CounterForm

    @classmethod
    def perform_mutate(cls, form, info):
        """
        add user before saving
        """
        obj = form.save(commit=False)
        obj.user = info.context.user
        obj.save()
        kwargs = {cls._meta.return_field_name: obj}
        return cls(errors=[], **kwargs)


class CounterDeleteMutation(graphene.Mutation):
    class Arguments:
        pk = graphene.Int()

    success = graphene.Boolean()

    def mutate(self, info, pk):

        Counter.objects.filter(id=pk).delete()
        return CounterDeleteMutation(success=True)



class Query(graphene.ObjectType):
    me = graphene.Field(MeObject)

    detail_total = graphene.Field(TotalType, id=graphene.Int())
    detail_counter = graphene.Field(CounterType, id=graphene.Int())

    list_total = graphene.List(TotalType)
    list_counter = graphene.List(CounterType)

    def resolve_me(self, info, **kwargs):
        if info.context.user.is_authenticated:
            return MeObject(username=info.context.user.username)
        return None

    def resolve_detail_total(self, info, **kwargs):
        id = kwargs.get("id")
        if id is not None:
            return Total.objects.get(pk=id)
        return None

    def resolve_detail_counter(self, info, **kwargs):
        id = kwargs.get("id")
        if id is not None:
            return Counter.objects.get(pk=id)
        return None

    def resolve_list_total(self, info, **kwargs):
        return Total.objects.filter(user=info.context.user)

    def resolve_list_counter(self, info, **kwargs):
        return Counter.objects.filter(user=info.context.user)


class Mutations(graphene.ObjectType):
    mutation_total = TotalMutation.Field()
    mutation_total_row = TotalRowMutation.Field()
    mutation_total_row_total = TotalRowTotalMutation.Field()
    mutation_counter = CounterMutation.Field()
    mutation_counter_row = CounterRowMutation.Field()

    mutation_delete_counter = CounterDeleteMutation.Field()
    mutation_delete_counter_row = CounterRowDeleteMutation.Field()
    mutation_delete_total = TotalDeleteMutation.Field()
    mutation_delete_total_row = TotalRowDeleteMutation.Field()
    mutation_delete_total_row_total = TotalRowTotalDeleteMutation.Field()


schema = graphene.Schema(query=Query, mutation=Mutations)
